import pypff
import pandas as pd
from html2text import html2text
import re
from datetime import datetime
import filetype
import uuid
import os


class PSTProcessor:
    def __init__(self, parent_dir: str = "./attachments") -> None:
        self.parent_dir = parent_dir

    
    def extract_attachment(self, attachment_obj):
        """
        """
        att_size = attachment_obj.get_size()
        file_blob = attachment_obj.read_buffer(att_size)

        return file_blob

    def get_attachment_type(self, blob):
        """
        """
        file_info = filetype.guess(blob)
        if file_info:
            return file_info.extension
        else:
            return None
     
    def save_attachment(self, 
                        blob, 
                        message_dir,
                        message_id,
                        attachment_id, 
                        blob_extension):
        
        attachment_dir = self.parent_dir + "/" + message_dir + "/" + message_id

        if blob_extension:
            attachment_path = attachment_dir + "/" + attachment_id + "." + blob_extension
        else: 
            attachment_path = attachment_dir + "/" + attachment_id

        if not os.path.exists(attachment_dir):
            os.makedirs(attachment_dir)
        with open(attachment_path, "wb+") as f:
            f.write(blob)

        return attachment_dir
    
    def clean_html_str(self, input_str):
        return re.sub(r'(\s*\\n+\s*)+', '\n', input_str[2:].replace(r"\r", ""))

    def parse_folder(self, base, date_filter):
        """
        """
        messages = []
        for folder in base.sub_folders:   
            if folder.number_of_sub_folders:
                messages += self.parse_folder(folder, date_filter)

            for message in folder.sub_messages:
                attachment_folder = None
                message_id = uuid.uuid4()
                try: 
                    number_of_attachments =  message.number_of_attachments
                except:
                    number_of_attachments = 0
                    
                if message.delivery_time >= date_filter:
                    
                    if number_of_attachments > 0:

                        for attachment_id in range(number_of_attachments):
                            
                            blob = self.extract_attachment(message.attachments[attachment_id])
                            blob_extension = self.get_attachment_type(blob)
                            attachment_folder = self.save_attachment(
                                                    blob=blob, 
                                                    message_dir=str(folder.name),
                                                    message_id=str(message_id),
                                                    attachment_id=str(attachment_id),
                                                    blob_extension=blob_extension)
                    messages.append({
                        "id": message_id,
                        "subject": message.subject,
                        "sender": message.sender_name,
                        "header": message.transport_headers,
                        "html_body": self.clean_html_str(html2text(str(message.html_body))),
                        "text_body": message.plain_text_body,
                        "creation_time": message.creation_time,
                        "submit_time": message.client_submit_time,
                        "delivery_time": message.delivery_time,
                        "number_of_attachments": number_of_attachments,
                        "attachments_folder": attachment_folder
                    })
               
        return messages
        
    
if __name__ == "__main__":

    pst_processor = PSTProcessor()
    pst_file = pypff.file()
    pst_file.open("./src/test.pst")
    
    root = pst_file.get_root_folder()
    
    date_filter = datetime(1959, 10, 1)
    messages = pst_processor.parse_folder(root, date_filter)

    df = pd.DataFrame(messages)
    df.to_csv("~/Desktop/pst_messages.csv")

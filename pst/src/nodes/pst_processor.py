import filetype
import os
import hashlib
from bs4 import BeautifulSoup


class PSTProcessor:
    """
    Personal Storage Table Processor
    """
    def __init__(self) -> None:
        pass
    
    def extract_attachment(self, attachment_obj):
        """
        Extract the content of an attachment object.
        """
        att_size = attachment_obj.get_size()
        file_blob = attachment_obj.read_buffer(att_size)

        return file_blob

    def get_attachment_type(self, blob):
        """
        Determine the file type for a given blob.
        """
        file_info = filetype.guess(blob)
        if file_info:
            return file_info.extension
        else:
            return None
     
    def save_attachment(self,
                        attachment_parent_dir,
                        attachment_blob, 
                        attachment_id, 
                        attachment_extension,
                        message_dir,
                        message_id) -> str:
        
        attachment_dir = "/".join((attachment_parent_dir, message_dir, message_id))
        if attachment_extension:
            attachment_path = "/".join((attachment_dir, attachment_id)) + "." + attachment_extension
        else: 
            attachment_path = "/".join((attachment_dir, attachment_id))

        if not os.path.exists(attachment_dir):
            os.makedirs(attachment_dir)
        with open(attachment_path, "wb+") as f:
            f.write(attachment_blob)

        return attachment_path

    def generate_unique_hash(self, text: str) -> str:
        """
        Generates a unique hash for a given text.
        
        Args:
            text (str): The text to generate the hash for.
        Returns: 
            str: A unique hash value.
        """
        standardized_text = text.lower().strip()
        hash_object = hashlib.sha256(standardized_text.encode())
        hash_value = str(hash_object.hexdigest())

        return hash_value

    def get_message_text(self, message) -> str:
        """
        Extract text for a given text.
        """
        if message.plain_text_body:
            return str(message.plain_text_body)
        else:
            return BeautifulSoup(str(message.html_body), "html.parser").text

    def get_pst_content(self, 
                        base_folder: str,  
                        include_attachment: bool,
                        attachment_parent_dir: str):
        """
        Traverses through the folders and items withing the given PST file. It retrives the content
        of each message and optionally extracts attachment if ìnclude_attachment` is set.

        Args:
            base_folder (str): personal storage table base (root) folder.
            include_attachment (bool): Flag indicating whether to extract attachment or not.
            attachment_parent_dir (str): Directory where extracted attachment will be saved.
        Return:
            List[dict]
        """

        messages = []
        for folder in base_folder.sub_folders:
  
            if folder.number_of_sub_folders:
                messages += self.get_pst_content(folder,
                                                 include_attachment,
                                                 attachment_parent_dir)

            for message in folder.sub_messages:

                attachments = []
                message_text = self.get_message_text(message)

                text2hash = str(message.subject) + message_text + str(message.creation_time) 
                message_id = self.generate_unique_hash(text2hash)

                try: 
                    number_of_attachments =  message.number_of_attachments
                except:
                    number_of_attachments = 0
                    
                if include_attachment:

                    for attachment_id in range(number_of_attachments):
                        
                        attachment_blob = self.extract_attachment(message.attachments[attachment_id])
                        attachment_extension = self.get_attachment_type(attachment_blob)
                        attachment_path = self.save_attachment(
                                                attachment_parent_dir=attachment_parent_dir,
                                                attachment_blob=attachment_blob,
                                                attachment_id=str(attachment_id),
                                                attachment_extension=attachment_extension,
                                                message_dir=str(folder.name),
                                                message_id=message_id)
                        attachments.append(attachment_path)

                    messages.append({
                        "id": message_id,
                        "subject": message.subject,
                        "sender": message.sender_name,
                        "header": message.transport_headers,
                        "message_text": message_text,
                        "creation_time": message.creation_time,
                        "submit_time": message.client_submit_time,
                        "delivery_time": message.delivery_time,
                        "number_of_attachments": number_of_attachments,
                        "attachments": attachments
                    })

                else:
                    messages.append({
                        "id": message_id,
                        "subject": message.subject,
                        "sender": message.sender_name,
                        "header": message.transport_headers,
                        "message_text": message_text,
                        "creation_time": message.creation_time,
                        "submit_time": message.client_submit_time,
                        "delivery_time": message.delivery_time
                    })
               
        return messages

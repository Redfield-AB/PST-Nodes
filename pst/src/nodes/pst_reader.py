import knime.extension as knext
from pst_processor import PSTProcessor
import pypff
import pandas as pd
from utils import get_sender_info, get_recipient_info



_category = knext.category(
    path="/community",
    level_id="pst",
    name="Redfield PST Nodes",
    description="Personal Storage Table Knime Nodes",
    icon="icons/redfield_logo.png"
)

@knext.node(name="PST Reader",
            node_type=knext.NodeType.SOURCE, 
            icon_path="icons/reader_icon.png", 
            category=_category)
@knext.output_table(name="Output Table", description="PST data")


class PSTReaderNode:
    """Retrives the content of a PST file
    
    This node reads PST (Personal Storage Table) files (.pst). 
    
    Starting from the root folder, the node traverses through each folder in the PST file. For each folder encountered, it examines its contents, which may include subfolders and individual messages. 
    Each message has a unique ID, which is used as the folder name where that message's attachments are stored.
    You can choose whether or not to extract attachments. 
    
    If attachments are extracted, the `Attachments` column will provide the exact location of each attachment object.
    """
    
    pst_path = knext.StringParameter(
        label="Input PST file path",
        description="The path of the PST file to read data from",
        default_value=""
    )

    include_attachment = knext.BoolParameter(
        label="Extract attachments",
        description="Check the box if you want to extract attachments",
        default_value=False
    )

    attachment_parent_dir = knext.StringParameter(
        label="Attachments path",
        description="Where would you like to save the attachments?",
        default_value=""
    )

    include_participant = knext.BoolParameter(
        label="Extract sender and recipient metadata",
        description="Check the box if you want to extract sender and recipient metadata",
        default_value=False
    )

    def configure(self, config_context):
        pass
    
    def execute(self, exec_context):

        if ".pst" not in self.pst_path:
            raise knext.InvalidParametersError(
                "Invalid PST file"
            )

        if self.include_attachment and self.attachment_parent_dir is "":
            raise knext.InvalidParametersError(
                "Attachment path is not specified"
            )
        
        pst_processor = PSTProcessor()
        pst_file = pypff.file()
        pst_file.open(self.pst_path)
        base_folder = pst_file.get_root_folder()

        exec_context.set_progress(progress=0.25)
        messages = pst_processor.get_pst_content(
            base_folder=base_folder,
            attachment_parent_dir=self.attachment_parent_dir,
            include_attachment=self.include_attachment
        )

        exec_context.set_progress(progress=0.75)
        df = pd.DataFrame(messages)
        
        if self.include_participant:
            df = df.apply(get_sender_info, axis=1)
            df = df.apply(get_recipient_info, axis=1)

        output_table = knext.Table.from_pandas(df)
        return output_table
    
import knime.extension as knext
from pst_processor import PSTProcessor
import pypff
import pandas as pd


@knext.node(name="PST Reader",
            node_type=knext.NodeType.SOURCE, 
            icon_path="icons/reader_icon.png", 
            category="/")
@knext.output_table(name="Output Table", description="PST data")


class PSTReaderNode:
    """ This is my first node in Knime develped purly in python"""
    
    pst_path = knext.StringParameter(
        label="Input PST file path",
        description="The file path for reading data.",
        default_value="",
    )
    
    include_attachment = knext.BoolParameter(
        label="Extract attachments",
        description="Check the box if you want to extract the attachments",
        default_value=True
    )
    attachment_parent_dir = knext.StringParameter(
        "Attachments path",
        "Where to save the attachments",
        default_value=""
    )

    def configure(self, config_context):
        pass
    
    def execute(self, exec_context):

        pst_processor = PSTProcessor()
        
        pst_file = pypff.file()
        pst_file.open(self.pst_path)
        base_folder = pst_file.get_root_folder()

        messages = pst_processor.get_pst_content(
            base_folder=base_folder,
            attachment_parent_dir=self.attachment_parent_dir,
            include_attachment=self.include_attachment
        )
        df = pd.DataFrame(messages)
        output_table = knext.Table.from_pandas(df)

        return output_table
    
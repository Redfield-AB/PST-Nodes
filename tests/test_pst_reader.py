from pst_extension.src.nodes.pst_processor import PSTProcessor
import pypff


def test_pst_reader():

    pst_processor = PSTProcessor()
    pst_file = pypff.file()
    pst_file.open("./sample.pst")
    base_folder = pst_file.get_root_folder()
    messages = pst_processor.get_pst_content(
        base_folder=base_folder,
        include_attachment=False,
        attachment_parent_dir=None
    )

    assert messages[0]["subject"] == "New message created by Aspose.Email for Java(Aspose.Email Evaluation)"
    assert "This is an evaluation copy of Aspose" in  messages[0]["message_text"]
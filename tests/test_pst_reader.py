from pst.src.nodes.pst_processor import PSTProcessor
from pst.src.nodes.utils import get_sender_info, get_recipient_info
import pandas as pd
import pypff


pst_processor = PSTProcessor()
pst_file = pypff.file()
pst_file.open("./sample.pst")
base_folder = pst_file.get_root_folder()
messages = pst_processor.get_pst_content(
    base_folder=base_folder,
    include_attachment=False,
    attachment_parent_dir=None
)

def test_pst_reader():

    assert messages[0]["subject"] == "New message created by Aspose.Email for Java(Aspose.Email Evaluation)"
    assert "This is an evaluation copy of Aspose" in  messages[0]["message_text"]


def test_email_extraction():

    df = pd.DataFrame(messages)
    df = df.apply(get_sender_info, axis=1)
    df = df.apply(get_recipient_info, axis=1)

    assert df["sender_email"][0] == "from@domain.com"
    assert df["recipient_email"][0] == "to1@domain.com"
    assert df["recipient_name"][0] == "Recipient 1"
    assert df['message_category'][0] == "myInbox"
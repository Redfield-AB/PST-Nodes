import re
from email.header import decode_header


sender_pattern = r'From:\s*(?:(.*?)\s*<([^>]+)>|([\w\.-]+@[\w\.-]+))'
recipient_patterns = [r'for\s*(?:(.*?)\s*<([^>]+)>|([\w\.-]+@[\w\.-]+))',
              r'To:\s*(?:(.*?)\s*<([^>]+)>|([\w\.-]+@[\w\.-]+))'
              ]
email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


def decode_value(value):

    decoded_parts = decode_header(value)
    decoded_value = ''.join(
        part.decode(encoding or 'utf-8') if isinstance(part, bytes) else part
        for part, encoding in decoded_parts
    )
    return decoded_value

def get_sender_info(row):
    """
    Extract sender email
    """
    try:
        sender_matches = re.findall(sender_pattern, row['header'])
        sender_email = [
            re.search(email_pattern, email).group(0)
            if re.search(email_pattern, email)
            else email_secondary
            for _, email, email_secondary in sender_matches]
        row["sender_email"] = sender_email[0]
    except:
        row["sender_email"] = None

    return row


def get_recipient_info(row):
    """
    Extract recipient name and email
    """
    try:
        recipient_matches = []
        for pattern in recipient_patterns:
            recipient_matches.extend(re.findall(pattern, row['header']))

        sender_info_list = [(decode_value(name), re.search(email_pattern, email).group(0)) 
                   if re.search(email_pattern, email) 
                   else ("", email_secondary) for name, email, email_secondary in recipient_matches]
        sender_info = sender_info_list[0]
        
        row['recipient_name'] = sender_info[0].strip("'").strip('"')
        row['recipient_email'] = sender_info[1].strip("'").strip('"')
    except:
        row['recipient_name'] = ""
        row['recipient_email'] = ""

    return row

    
    
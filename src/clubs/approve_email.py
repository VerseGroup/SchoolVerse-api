from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_approval_email(key, from_email, to_email, club_name, leaders, club_description, admin, link):
    try:
        sg = SendGridAPIClient(key)
    except:
        return {
            "status": "error authentificating with sendgrid"
        }

    subject = f"[ACTION REQUIRED] Club {club_name} requests approval"
    body = f"""Hello, {admin},
    
    The club {club_name} has requested approval. 

    Leaders: {leaders}
    Description: {club_description}
    
    Please visit the following link to approve or deny the club:
    {link}

    Thank you,
    Paul from VerseGroup, LLC

    This is an automated email. Replies will be sent to 'pevans@versegroup.tech'. 

    """

    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=body)
    try:
        response = sg.send(message)
        return {
            "status": str(response.status_code),
        }
    except Exception as e:
        return {"error": str(e)}


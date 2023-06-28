from sqlalchemy import and_, or_

from db.models import Email


def get_condition_mapping(value):
    return {
        "From": {
            "contains": Email.sender.ilike(f"%{value}%"),
            "not contains": ~Email.sender.ilike(f"%{value}%"),
            "equals": Email.sender == value,
            "does not equal": Email.sender != value,
        },
        "To": {
            "contains": Email.recipient.ilike(f"%{value}%"),
            "not contains": ~Email.recipient.ilike(f"%{value}%"),
            "equals": Email.recipient == value,
            "does not equal": Email.recipient != value,
        },
        "Subject": {
            "contains": Email.subject.ilike(f"%{value}%"),
            "not contains": ~Email.subject.ilike(f"%{value}%"),
            "equals": Email.subject == value,
            "does not equal": Email.subject != value,
        },
        "Received Date": {
            "less than": Email.received_date < value,
            "greater than": Email.received_date > value,
        },
    }


def read_email_from_db(session, rule):
    conditions = []
    query = session.query(Email)
    for condition in rule["conditions"]:
        field = condition["field"]
        predicate = condition["predicate"]
        value = condition["value"]

        field_mapping = get_condition_mapping(value)

        if field in field_mapping and predicate in field_mapping[field]:
            condition_expr = field_mapping[field][predicate]
            conditions.append(condition_expr)

    if conditions and rule["predicate"] == "All":
        query = query.filter(and_(*conditions))
    elif conditions and rule["predicate"] == "Any":
        query = query.filter(or_(*conditions))

    query_emails = query.all()
    session.close()

    emails = [
        {
            "email_id": email.email_id,
            "subject": email.subject,
            "sender": email.sender,
            "recipient": email.recipient,
            "received_date": email.received_date,
        }
        for email in query_emails
    ]

    return emails


# Bulk create emails
def bulk_create_emails(session, emails_data):
    emails = [Email(**email_data) for email_data in emails_data]
    session.bulk_save_objects(emails)
    session.commit()
    session.close()

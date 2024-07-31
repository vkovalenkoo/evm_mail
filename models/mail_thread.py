from odoo import models, api
from markupsafe import Markup

class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.model
    def message_post(self, **kwargs):
        # Extract the message body if it exists
        body = kwargs.get('body', '')

        if isinstance(body, Markup):
            body = f'<html><p>{body.unescape()}</p>'

        new_attachments = []
        if 'attachment_ids' in kwargs:
            attachment_ids = kwargs['attachment_ids']

            for attachment_id in attachment_ids:
                attachment_record = self.env['ir.attachment'].browse(attachment_id)
                if attachment_record.mimetype.startswith('image/'):
                    # Generate the image tag
                    image_tag = f'<img src="/web/content/{attachment_record.id}" alt="{attachment_record.name}"/>'
                    # Append the image tag inside the body div
                    body += image_tag
                else:
                    new_attachments.append(attachment_id)

        body += '</html>'

        kwargs.update({
            'body': body,
            'body_is_html': True,
            'attachment_ids': new_attachments,
        })

        return super(MailThread, self).message_post(**kwargs)


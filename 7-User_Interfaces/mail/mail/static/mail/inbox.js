document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Handle form submission
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function send_email(event) {
  event.preventDefault();

  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
  .then(response => response.json())
  .then(result => {
    // Load the sent mailbox after sending the email
    load_mailbox('sent');
  });
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Fetch the emails for the mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email => {
      const emailDiv = document.createElement('div');
      emailDiv.className = 'email';
      emailDiv.innerHTML = `
        <div><strong>${email.sender}</strong></div>
        <div>${email.subject}</div>
        <div>${email.timestamp}</div>
      `;
      emailDiv.style.backgroundColor = email.read ? 'gray' : 'white';
      emailDiv.addEventListener('click', () => view_email(email.id));
      document.querySelector('#emails-view').append(emailDiv);
    });
  });
}

function view_email(email_id) {
  // Show the email view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  // Fetch the email details
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    document.querySelector('#email-view').innerHTML = `
      <div><strong>From:</strong> ${email.sender}</div>
      <div><strong>To:</strong> ${email.recipients.join(', ')}</div>
      <div><strong>Subject:</strong> ${email.subject}</div>
      <div><strong>Timestamp:</strong> ${email.timestamp}</div>
      <hr>
      <div>${email.body}</div>
      <button id="archive">${email.archived ? 'Unarchive' : 'Archive'}</button>
      <button id="reply">Reply</button>
    `;

    // Mark the email as read
    fetch(`/emails/${email_id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    });

    // Archive/Unarchive email
    document.querySelector('#archive').addEventListener('click', () => {
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: !email.archived
        })
      })
      .then(() => load_mailbox('inbox'));
    });

    // Reply to email
    document.querySelector('#reply').addEventListener('click', () => {
      compose_email();
      document.querySelector('#compose-recipients').value = email.sender;
      document.querySelector('#compose-subject').value = email.subject.startsWith('Re:') ? email.subject : `Re: ${email.subject}`;
      document.querySelector('#compose-body').value = `On ${email.timestamp}, ${email.sender} wrote:\n${email.body}`;
    });
  });
}
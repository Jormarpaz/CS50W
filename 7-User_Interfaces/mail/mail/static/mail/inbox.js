console.log('inbox.js loaded');

document.addEventListener('DOMContentLoaded', function() {
  console.log('DOM fully loaded and parsed');
  
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
  console.log('Composing new email');
  
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

  console.log('Sending email:', { recipients, subject, body });

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => {
    if (!response.ok) {
      return response.json().then(error => { throw new Error(error.error); });
    }
    return response.json();
  })
  .then(result => {
    console.log('Email sent result:', result);
    if (result.error) {
      console.log(result.error);
    } else {
      // Load the sent mailbox after sending the email
      load_mailbox('sent');
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

function load_mailbox(mailbox) {
  console.log(`Loading mailbox: ${mailbox}`);
  
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
    console.log('Emails:', emails);
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
  console.log(`Viewing email: ${email_id}`);
  
  // Show the email view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  // Fetch the email details
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    console.log('Email details:', email);
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
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    });

    // Archive/Unarchive email
    document.querySelector('#archive').addEventListener('click', () => {
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: !email.archived
        }),
        headers: {
          'Content-Type': 'application/json'
        }
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
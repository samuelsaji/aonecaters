/**
 * A-one Caterers website enquiries -> Google Sheet + email alert
 *
 * Setup (one time):
 * 1. Create a Google Sheet, e.g. "A-one Website Enquiries".
 * 2. In the sheet: Extensions > Apps Script. Delete the sample code and paste this file.
 * 3. Set NOTIFY_EMAIL below to the address that should get each enquiry.
 * 4. Deploy > New deployment > type "Web app".
 *      Execute as: Me
 *      Who has access: Anyone
 *    Click Deploy and approve the permissions.
 * 5. Copy the Web app URL (ends in /exec) into SCRIPT_URL in assets/js/main.js.
 */

const NOTIFY_EMAIL = 'CHANGE_ME@gmail.com'; // comma-separate for several people
const SHEET_NAME = 'Enquiries';
const HEADERS = ['Received', 'Name', 'Phone', 'Event', 'Event date', 'Guests', 'Venue / location', 'Menu ideas or questions', 'WhatsApp link'];

function doPost(e) {
  const p = (e && e.parameter) || {};

  // Spam trap: real visitors never fill this hidden field.
  if (p.website) return json_({ ok: true });

  const clean = (v, max) => {
    let s = String(v || '').trim().slice(0, max || 500);
    if (/^[=+\-@]/.test(s)) s = "'" + s; // stop formulas being injected into the sheet
    return s;
  };
  const row = {
    name: clean(p.name, 120),
    phone: clean(p.phone, 40),
    event: clean(p.event, 80),
    date: clean(p.date, 20),
    guests: clean(p.guests, 10),
    venue: clean(p.venue, 200),
    message: clean(p.message, 3000),
  };
  if (!row.name || !row.phone) return json_({ ok: false, error: 'missing fields' });

  let digits = row.phone.replace(/\D/g, '');
  if (digits.length === 10) digits = '91' + digits;
  const wa = 'https://wa.me/' + digits;

  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  let sheetUrl;
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    sheetUrl = ss.getUrl();
    const sh = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
    if (sh.getLastRow() === 0) {
      sh.appendRow(HEADERS);
      sh.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold');
      sh.setFrozenRows(1);
    }
    sh.appendRow([new Date(), row.name, row.phone, row.event, row.date, row.guests, row.venue, row.message, wa]);
  } finally {
    lock.releaseLock();
  }

  MailApp.sendEmail({
    to: NOTIFY_EMAIL,
    subject: 'New enquiry: ' + row.event + (row.date ? ' on ' + row.date : '') + ' - ' + row.name,
    body:
      'New enquiry from the A-one Caterers website\n\n' +
      'Name: ' + row.name + '\n' +
      'Phone: ' + row.phone + '\n' +
      'Event: ' + row.event + '\n' +
      'Date: ' + (row.date || 'Not decided') + '\n' +
      'Guests: ' + (row.guests || '-') + '\n' +
      'Venue: ' + (row.venue || '-') + '\n\n' +
      'Menu ideas / questions:\n' + (row.message || '-') + '\n\n' +
      'Reply on WhatsApp: ' + wa + '\n' +
      'All enquiries: ' + sheetUrl,
  });

  return json_({ ok: true });
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

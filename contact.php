<?php
// Banda Bookkeepers — bookkeeping enquiry form handler (hand-edited; not generated).
// Sends website enquiries to the Think Mybiz practice mailbox. No data is stored on the server.
date_default_timezone_set('Africa/Johannesburg');
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

$TO   = 'accounts@thinkmybiz.co.za';
$FROM = 'accounts@thinkmybiz.co.za'; // existing practice mailbox: Hostinger drops PHP mail from addresses that do not exist

function out($code, $arr) { http_response_code($code); echo json_encode($arr); exit; }

// Authenticated SMTP for accounts@ (better inbox delivery than PHP mail()).
// Credentials live OUTSIDE every web root and outside Git. This site reuses the practice's existing file:
//   first  <domains>/bandabookkeepers.com/.tmb-smtp.php   (if one is ever created for this site)
//   then   <domains>/thinkmybiz.co.za/.tmb-smtp.php       (same hosting account, same mailbox)
// If neither is readable, mail() is used. An SMTP failure is logged and mail() is tried once.
$SMTP = null;
foreach ([dirname(__DIR__) . '/.tmb-smtp.php', dirname(__DIR__, 2) . '/thinkmybiz.co.za/.tmb-smtp.php'] as $f) {
  if (is_readable($f)) { $c = include $f; if (is_array($c) && !empty($c['host']) && !empty($c['user']) && isset($c['pass'])) { $SMTP = $c; break; } }
}

function smtp_send(array $c, string $to, string $subjectEnc, string $body, array $headers): bool {
  $ssl = ['verify_peer' => true, 'verify_peer_name' => true, 'peer_name' => $c['host']];
  if (!empty($c['cafile'])) $ssl['cafile'] = $c['cafile'];
  $fp = @stream_socket_client('ssl://' . $c['host'] . ':' . (int)($c['port'] ?? 465), $en, $es, 15,
                              STREAM_CLIENT_CONNECT, stream_context_create(['ssl' => $ssl]));
  if (!$fp) { error_log("bandabookkeepers contact.php SMTP connect failed: $es"); return false; }
  stream_set_timeout($fp, 15);
  $step = function ($line, array $ok) use ($fp) {
    if ($line !== null) fwrite($fp, $line . "\r\n");
    $resp = '';
    while (($l = fgets($fp, 1024)) !== false) { $resp .= $l; if (strlen($l) < 4 || $l[3] !== '-') break; }
    if (!in_array((int)substr($resp, 0, 3), $ok, true)) { error_log('bandabookkeepers contact.php SMTP: ' . trim($resp)); return false; }
    return true;
  };
  $msg = implode("\r\n", array_merge([
      'Date: ' . date('r'), 'To: <' . $to . '>', 'Subject: ' . $subjectEnc,
      'Message-ID: <' . bin2hex(random_bytes(12)) . '@bandabookkeepers.com>', 'MIME-Version: 1.0',
      'Content-Transfer-Encoding: base64'], $headers)) . "\r\n\r\n" . rtrim(chunk_split(base64_encode($body), 76, "\r\n"));
  $ok = $step(null, [220]) && $step('EHLO bandabookkeepers.com', [250]) && $step('AUTH LOGIN', [334])
     && $step(base64_encode($c['user']), [334]) && $step(base64_encode($c['pass']), [235])
     && $step('MAIL FROM:<' . $c['user'] . '>', [250]) && $step('RCPT TO:<' . $to . '>', [250, 251])
     && $step('DATA', [354]) && $step($msg . "\r\n.", [250]);
  @fwrite($fp, "QUIT\r\n"); fclose($fp);
  return $ok;
}

function send_mail(string $to, string $subjectEnc, string $body, array $headers, string $from): bool {
  global $SMTP;
  if ($SMTP && smtp_send($SMTP, $to, $subjectEnc, $body, $headers)) return true;
  return @mail($to, $subjectEnc, $body, implode("\r\n", $headers), '-f' . $from);
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') out(405, ['ok' => false, 'error' => 'Method not allowed.']);

function clean($k, $max) {
  $v = isset($_POST[$k]) ? trim((string)$_POST[$k]) : '';
  $v = str_replace(["\r", "\0"], '', $v);
  return mb_substr($v, 0, $max);
}
function one($s) { return preg_replace('/[\n]+/', ' ', $s); }
function pick($k, array $allowed) { $v = clean($k, 80); return in_array($v, $allowed, true) ? $v : ''; }

$name     = clean('name', 120);
$email    = clean('email', 160);
$phone    = clean('phone', 40);
$business = clean('business', 160);
$town     = clean('town', 80);
$entity   = pick('entity', ['Sole trader', '(Pty) Ltd', 'Close corporation (CC)', 'Trust', 'NPO / NPC', 'Partnership', 'Not registered yet']);
$volume   = pick('volume', ['Under 100', '100 to 300', 'Over 300', 'Not sure']);
$accounts = pick('accounts', ['1', '2 to 3', '4 or more']);
$vat      = pick('vat', ['Yes', 'No', 'Not sure']);
$staff    = pick('staff', ['None', '1 to 5', '6 to 20', '21 to 50', 'Over 50']);
$software = clean('software', 80);
$status   = pick('status', ['Up to date', 'Behind by a few months', 'Behind by a year or more', 'No books kept yet']);
$package  = pick('package', ['Not sure yet', 'Starter', 'Business', 'Business + Payroll', 'Clean-up (once-off)']);
$message  = clean('message', 5000);
$consent  = !empty($_POST['consent']);

if ($name === '') out(422, ['ok' => false, 'error' => 'Please give your name.']);
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) out(422, ['ok' => false, 'error' => 'Please enter a valid email address.']);
if (!preg_match('/\d{3}/', $phone)) out(422, ['ok' => false, 'error' => 'Please enter a phone number so we can call you back.']);
if ($entity === '' || $volume === '' || $status === '') out(422, ['ok' => false, 'error' => 'Please answer the business type, monthly transactions and books status questions.']);
if (!$consent) out(422, ['ok' => false, 'error' => 'Please confirm that we may use your details to respond.']);

// Spam checks run after validation, so a person is never shown a false "sent".
if (!empty($_POST['hp_check'])) out(422, ['ok' => false, 'error' => 'Your enquiry could not be sent. Please email accounts@thinkmybiz.co.za or call 066 210 5631.']);
$ts = isset($_POST['ts']) ? (int)$_POST['ts'] : 0;
if ($ts > 0 && (round(microtime(true) * 1000) - $ts) < 2000) out(422, ['ok' => false, 'error' => 'Please take a moment to check your details, then send again.']);

// Lead fit: regular monthly activity + an ongoing service = qualified.
$qualified = ($volume !== 'Under 100' || $accounts !== '1' || $vat === 'Yes' || ($staff !== '' && $staff !== 'None')) && $package !== 'Clean-up (once-off)';
$fit = $qualified ? 'Qualified — ongoing monthly bookkeeping' : ($package === 'Clean-up (once-off)' || strpos($status, 'Behind') === 0 ? 'Clean-up quote' : 'Small / starter — review');

$name1 = one($name);
$subject = 'Bookkeeping enquiry: ' . ($package ?: 'Not sure yet') . ' — ' . $name1 . ($business !== '' ? ' (' . one($business) . ')' : '');
$body = "New bookkeeping enquiry from bandabookkeepers.com\n\n"
      . "Lead fit: $fit\n\n"
      . "Name: $name1\nEmail: $email\nPhone: " . one($phone) . "\nBusiness: " . one($business) . "\nTown: " . one($town) . "\n\n"
      . "Business type: $entity\nMonthly transactions: $volume\nBank/card accounts: $accounts\nVAT registered: $vat\n"
      . "Employees on payroll: $staff\nAccounting software: " . one($software) . "\nBooks status: $status\nPackage of interest: $package\n"
      . "Received: " . date('Y-m-d H:i') . " (SAST)\n\nMessage:\n" . ($message !== '' ? $message : '(none)') . "\n\n"
      . "The sender consented to their details being used to respond to this enquiry (POPIA).\n";

$headers = [
  'From: Banda Bookkeepers Website <' . $FROM . '>',
  'Reply-To: ' . $name1 . ' <' . $email . '>',
  'Content-Type: text/plain; charset=UTF-8',
  'X-Mailer: bandabookkeepers.com',
];
$sent = send_mail($TO, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers, $FROM);
if (!$sent) out(500, ['ok' => false, 'error' => 'Your enquiry could not be sent. Please email accounts@thinkmybiz.co.za or WhatsApp 066 210 5631.']);

// One automatic acknowledgement to the enquirer (no marketing). Failure here does not affect the enquiry.
$first = trim(explode(' ', $name1)[0]);
$ack = "Dear " . ($first !== '' ? $first : 'Sir/Madam') . ",\n\n"
     . "Thank you for contacting Banda Bookkeepers. We have received your bookkeeping enquiry and will contact you to arrange a free consultation.\n\n"
     . "To help us prepare, you may reply with your latest bank statement period and the accounting software you use, if any. "
     . "Please ask us for a secure route before sending identity numbers or full statements.\n\n"
     . "Telephone / WhatsApp: 066 210 5631\nEmail: accounts@thinkmybiz.co.za\nWebsite: https://bandabookkeepers.com\n\n"
     . "Kind regards\nBanda Bookkeepers\nPart of Think Mybiz Accountants and Tax Practitioners (Pty) Ltd\n\n"
     . "You received this one-off email because you submitted an enquiry on bandabookkeepers.com. It is not a marketing message.\n";
$ackHeaders = [
  'From: Banda Bookkeepers <' . $FROM . '>',
  'Reply-To: Banda Bookkeepers <' . $TO . '>',
  'Content-Type: text/plain; charset=UTF-8',
  'Auto-Submitted: auto-replied',
  'X-Mailer: bandabookkeepers.com',
];
send_mail($email, '=?UTF-8?B?' . base64_encode('We received your bookkeeping enquiry — Banda Bookkeepers') . '?=', $ack, $ackHeaders, $FROM);
out(200, ['ok' => true]);

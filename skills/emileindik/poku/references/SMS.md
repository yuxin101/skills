# SMS Flow — Steps A → B → C

## Step A: Resolve the Phone Number

- **Raw number** (e.g. `917-257-7580`) — strip formatting, prepend country code (+1 for US & Canada). Result: `+19172577580`
- **Contact name** — ask the user for the number directly; do not guess
- **Business name only** — use the search tool to find the number, then confirm with the user

→ Output: `<normalized number>` in E.164 format, used in Step C.

---

## Step B: Draft and Confirm

Use the **SMS Templates** section below to draft the message. Show it clearly:

> **Here's the draft:**
> "[message body]"
>
> Sending to [number] — good to go?

Do not send until the user confirms.

---

## Step C: Send the Text

```bash
curl -s -X POST \
  -H "Authorization: Bearer $POKU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"message": "<message body>", "to": "<normalized number>"}' \
  https://api.pokulabs.com/phone/sms
```

Once sent, confirm: "Done — your text was sent to [number]."

For error codes, see `references/API.md`.

---

# SMS Templates

Use the closest matching template and adapt it — an exact match is not required.

If no template fits, use **General / Other** as a starting point.

**Placeholder rules:** All placeholders appear in `[brackets]`. Replace every placeholder with a real value. Never leave a placeholder unfilled.

---

### Scheduling

```
Hi, I'm reaching out on behalf of [user name] to coordinate [activity] for you both. Let me know a few times that you're available [timeframe]!
```

---

### Follow-Up After a Call

```
Hi, this is [user name] following up on our recent conversation about [topic]. [One sentence summary of next step or ask.] Feel free to reply here or call back at your convenience.
```

---

### General / Other

```
Hi, this is a message on behalf of [user name]. [State the purpose in one or two plain sentences.] [Optional: include a call to action — reply, call back, confirm, etc.] Thank you.
```

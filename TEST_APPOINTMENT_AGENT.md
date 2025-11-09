# 🧪 Testing the Enhanced Appointment Agent

## ✅ Servers Status

Both servers are now running:
- **Backend:** http://localhost:8000 ✅
- **Frontend:** Check terminal output for port (likely 8082 or 5173)

---

## 🎯 Test Plan

Test all 5 appointment operations through the chat interface.

---

## 📋 Test 1: List Appointments

### **What to Type:**
```
Show me my appointments
```

### **Alternative Phrases:**
```
What appointments do I have?
List my appointments
Show my upcoming appointments
Do I have any appointments?
```

### **Expected Response:**
```
📅 Your Appointments (X total):

🟢 Appointment #5
   • Doctor: Dr. Sarah Johnson
   • Type: Consultation
   • Date: Monday, November 11, 2024 at 02:00 PM
   • Status: Scheduled
   • Reason: Annual check-up
   • Location: Main Clinic

💡 You can cancel or reschedule any appointment by telling me the appointment number.
```

**Or if no appointments:**
```
You don't have any appointments scheduled yet. Would you like to book one?
```

✅ **Pass Criteria:**
- Shows formatted list with all appointment details
- Includes appointment IDs
- Status indicators (🟢 for scheduled, ✅ for confirmed, etc.)

---

## ➕ Test 2: Create Appointment

### **What to Type:**
```
I want to book an appointment
```

### **Expected Conversation:**
```
You: I want to book an appointment

Bot: I'd be happy to help you schedule an appointment! To get started, could you please tell me:
1. What type of appointment do you need? (consultation, follow-up, check-up, etc.)
2. When would you prefer? (date and time)
3. What is the reason for your visit?

You: Consultation with Dr. Johnson tomorrow at 2pm for headache

Bot: ✅ Appointment booked successfully!

📅 Appointment Details:
- Doctor: Dr. Sarah Johnson
- Type: Consultation
- Date & Time: [Tomorrow's date] at 02:00 PM
- Duration: 30 minutes
- Location: Main Clinic
- Reason: headache

You'll receive a reminder 24 hours before your appointment.
```

### **Quick Booking (One Message):**
```
Book appointment with Dr. Chen tomorrow at 3pm for follow-up
```

✅ **Pass Criteria:**
- Agent extracts all details from natural language
- Creates appointment in database
- Returns appointment ID
- Shows green confirmation card in UI

---

## ❌ Test 3: Cancel Appointment

### **What to Type:**
```
Cancel appointment #5
```

### **Alternative Phrases:**
```
Delete appointment 5
Remove appointment #5
Cancel my appointment number 5
```

### **Expected Response:**
```
❌ Appointment Cancelled

Appointment #5 has been successfully cancelled.

Cancelled Appointment Details:
• Doctor: Dr. Sarah Johnson
• Type: Consultation
• Was scheduled for: Monday, November 11, 2024 at 02:00 PM
• Previous status: Scheduled

If you'd like to book a new appointment, just let me know!
```

✅ **Pass Criteria:**
- Finds appointment by ID
- Updates status to 'cancelled' in database
- Shows cancellation confirmation
- Prevents cancelling non-existent or already cancelled appointments

### **Error Test:**
```
Cancel appointment #999
```

**Expected:**
```
I couldn't find appointment #999 for your account. Please check the appointment number.
```

---

## 📝 Test 4: Update/Reschedule Appointment

### **What to Type:**
```
Reschedule appointment #3 to tomorrow at 3pm
```

### **Alternative Phrases:**
```
Change appointment 3 to 3pm tomorrow
Move my appointment #3 to next week
Update appointment 3
```

### **Expected Response:**
```
✅ Appointment Updated

Appointment #3 has been successfully updated.

Updated Details:
• Doctor: Dr. Michael Chen
• Type: Follow-up
• New Date & Time: Tuesday, November 12, 2024 at 03:00 PM
• Duration: 30 minutes
• Location: Virtual
• Status: Scheduled

📅 Changed from: Monday, November 11, 2024 at 10:00 AM

You'll receive a reminder 24 hours before your appointment.
```

✅ **Pass Criteria:**
- Parses new date/time from natural language
- Updates appointment in database
- Shows both old and new times
- Maintains other appointment details

---

## 🕐 Test 5: Show Available Slots

### **What to Type:**
```
What times are available this week?
```

### **Alternative Phrases:**
```
Show me available slots
When can I book an appointment?
What times are free?
Show available appointments
```

### **Expected Response:**
```
Here are the available appointment slots:

📅 Available Appointments:
1. Monday, November 11 at 09:00 AM
2. Monday, November 11 at 09:30 AM
3. Monday, November 11 at 10:00 AM
4. Monday, November 11 at 10:30 AM
5. Monday, November 11 at 11:00 AM
...
```

✅ **Pass Criteria:**
- Shows formatted list of available slots
- Only weekdays (Mon-Fri)
- Only business hours (9 AM - 5 PM)
- Skips past times
- Blue card display in UI

---

## 🎨 UI/UX Checks

### **Green Success Card**
When appointment is booked or updated successfully:
- ✅ Green border
- ✅ Checkmark icon
- ✅ "Appointment Booked" or "Appointment Updated" title
- ✅ All appointment details displayed
- ✅ Icons for calendar, doctor, time, location

### **Red Error Card**
When there's an error:
- ❌ Red border
- ❌ Error message clearly displayed
- ❌ Helpful suggestion for what to do

### **Blue Info Card**
For available slots:
- 📅 Blue border
- 📅 "Available Time Slots" title
- 📅 List of slots with calendar icons

---

## 🔐 Security Tests

### **Test 1: Authentication Required**

Log out and try to send a message:

**Expected:** Error about authentication required

### **Test 2: Can't Access Other's Appointments**

Try to cancel someone else's appointment:
```
Cancel appointment #[someone_else's_id]
```

**Expected:** "Appointment not found" (because it's not yours)

### **Test 3: Can Only See Own Appointments**
```
Show my appointments
```

**Expected:** Only YOUR appointments, not anyone else's

---

## 🐛 Edge Cases to Test

### **Test 1: Cancel Already Cancelled**
```
Cancel appointment #5
[Then try again]
Cancel appointment #5
```

**Expected:** "Appointment #5 is already cancelled."

### **Test 2: Update Cancelled Appointment**
```
Reschedule appointment #5 to tomorrow
```

**Expected:** "Appointment #5 is cancelled. Would you like to book a new one instead?"

### **Test 3: Invalid Appointment ID**
```
Cancel appointment #99999
```

**Expected:** "I couldn't find appointment #99999..."

### **Test 4: Past Date Booking**
```
Book appointment yesterday at 2pm
```

**Expected:** Agent should recognize it's in the past and ask for a valid date

### **Test 5: Natural Language Dates**
```
Book appointment next Monday at 2pm
Book for tomorrow afternoon
Schedule me for this Friday morning
```

**Expected:** Agent correctly interprets dates

---

## 📊 Quick Test Checklist

Copy this to test systematically:

```
□ Test 1: List appointments
   Command: "Show my appointments"
   Result: _______________

□ Test 2: Create appointment
   Command: "Book appointment tomorrow at 2pm"
   Result: _______________
   Appointment ID: _______________

□ Test 3: Cancel appointment
   Command: "Cancel appointment #[ID from Test 2]"
   Result: _______________

□ Test 4: Create another appointment
   Command: "Book with Dr. Johnson Friday at 3pm"
   Result: _______________
   Appointment ID: _______________

□ Test 5: Update appointment
   Command: "Reschedule appointment #[ID] to Monday 4pm"
   Result: _______________

□ Test 6: List appointments again
   Command: "Show my appointments"
   Result: _______________

□ Test 7: Show available slots
   Command: "What times are available?"
   Result: _______________

□ Test 8: Cancel invalid ID
   Command: "Cancel appointment #99999"
   Result: _______________

□ Test 9: General chat still works
   Command: "What is a fever?"
   Result: _______________
```

---

## 🔧 Troubleshooting

### **Issue: Agent responds but doesn't book**

**Check:**
1. Look for JSON in the AI response
2. Check console for errors
3. Verify OpenAI API key is valid

### **Issue: "Show appointments" doesn't work**

**Check:**
1. Intent detection is working: Should return 'list'
2. Look in terminal for errors
3. Check database has appointments table

### **Issue: Frontend shows appointment data as text**

**Check:**
1. ChatMessage component has appointmentData prop
2. appointment_data is in the response
3. Check browser console for React errors

### **Issue: Can't cancel by ID**

**Check:**
1. Message includes the number: "#5" or "5"
2. Appointment belongs to logged-in user
3. Appointment exists and isn't already cancelled

---

## 🎯 Success Criteria

All tests should:
✅ Execute without errors
✅ Display formatted responses
✅ Update database correctly
✅ Show appropriate UI cards
✅ Maintain security (user isolation)
✅ Handle errors gracefully

---

## 📱 Access the Application

**Frontend:** Check your terminal for the Vite dev server output. It should show:
```
VITE v5.x.x ready in XXX ms
➜ Local: http://localhost:XXXX/
```

Open that URL in your browser!

**Backend API Docs:** http://localhost:8000/docs
(Note: Should NOT see /appointments endpoints, only /chat)

---

## 🎉 When All Tests Pass

You have successfully:
✅ Enhanced the appointment agent with full CRUD
✅ Removed the REST API
✅ Unified all operations through natural language
✅ Maintained security and data integrity
✅ Created a better user experience

**Your Carely AI appointment system is now fully AI-powered!** 🚀

---

## 📝 Report Any Issues

If any test fails, note:
1. What command you typed
2. What you expected
3. What actually happened
4. Any error messages
5. Browser console logs

This will help debug any issues!


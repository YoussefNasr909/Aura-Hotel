import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_URL = "http://127.0.0.1:5000"


@pytest.fixture()
def base_url():
    return BASE_URL


@pytest.fixture()
def driver():
    options = Options()

    # HEADLESS MODE: Enabled by default for faster tests
    # Set HEADLESS=0 in terminal to see the browser window
    if os.getenv("HEADLESS", "1") != "0":
        options.add_argument("--headless=new")

    # Window size
    options.add_argument("--window-size=1400,900")
    
    # === PERFORMANCE OPTIMIZATIONS ===
    # Faster page load - don't wait for all resources
    options.page_load_strategy = "eager"
    
    # Disable unnecessary features
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    
    # Disable images for faster loading (optional - uncomment if needed)
    # options.add_argument("--blink-settings=imagesEnabled=false")
    
    # Reduce logging
    options.add_argument("--log-level=3")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    
    # Reduce implicit wait time
    drv.implicitly_wait(2)

    yield drv
    drv.quit()


def send_test_notification(run_data):
    """
    Send email notification after tests complete (pass or fail).
    
    Configure via environment variables:
    - NOTIFY_EMAIL_TO: Recipient email address
    - NOTIFY_EMAIL_FROM: Sender email (Gmail address)
    - NOTIFY_EMAIL_PASSWORD: Gmail App Password (not regular password)
    
    To get a Gmail App Password:
    1. Enable 2-Factor Authentication on your Google account
    2. Go to https://myaccount.google.com/apppasswords
    3. Generate a new app password for "Mail"
    """
    email_to = os.getenv("NOTIFY_EMAIL_TO")
    email_from = os.getenv("NOTIFY_EMAIL_FROM")
    email_password = os.getenv("NOTIFY_EMAIL_PASSWORD")
    
    if not all([email_to, email_from, email_password]):
        print("\n[NOTIFICATION] Email not configured. Set NOTIFY_EMAIL_TO, NOTIFY_EMAIL_FROM, NOTIFY_EMAIL_PASSWORD")
        return False
    
    # Determine if tests passed or failed
    is_success = run_data['failed'] == 0 and run_data['exitstatus'] == 0
    
    try:
        # Create message
        msg = MIMEMultipart("alternative")
        
        if is_success:
            msg["Subject"] = f"✅ AURA Hotel Tests PASSED - All {run_data['passed']} tests successful!"
            status_emoji = "✅"
            status_text = "All Tests Passed!"
            status_color = "#4ade80"  # Green
            status_message = "All automated tests have passed successfully."
        else:
            msg["Subject"] = f"🔴 AURA Hotel Tests FAILED - {run_data['failed']} failures"
            status_emoji = "🔴"
            status_text = "Tests Failed!"
            status_color = "#f87171"  # Red
            status_message = "Some automated tests have failed. Please check the report."
        
        msg["From"] = email_from
        msg["To"] = email_to
        
        # Plain text version
        text = f"""
AURA Hotel Test Results
=====================================

Status: {"PASSED" if is_success else "FAILED"}
Test Run: {run_data['timestamp']}

Results:
- Total: {run_data['total']}
- Passed: {run_data['passed']}
- Failed: {run_data['failed']}
- Skipped: {run_data['skipped']}

{"All tests passed!" if is_success else "Please check the test report for details."}
        """
        
        # HTML version
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #000814; color: #fff7ce; padding: 20px;">
            <div style="max-width: 500px; margin: 0 auto; background: #001d3d; border-radius: 12px; padding: 20px; border: 1px solid #003566;">
                <h2 style="color: {status_color}; margin-top: 0;">{status_emoji} {status_text}</h2>
                <p style="color: #a5d1ff;">{status_message}</p>
                
                <div style="background: #003566; padding: 15px; border-radius: 8px; margin: 15px 0;">
                    <table style="width: 100%; color: #fff7ce;">
                        <tr>
                            <td style="padding: 5px 0;">📅 Timestamp:</td>
                            <td style="font-weight: bold;">{run_data['timestamp']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px 0;">📊 Total Tests:</td>
                            <td style="font-weight: bold;">{run_data['total']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px 0;">✅ Passed:</td>
                            <td style="color: #4ade80; font-weight: bold;">{run_data['passed']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px 0;">❌ Failed:</td>
                            <td style="color: #f87171; font-weight: bold;">{run_data['failed']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px 0;">⏭️ Skipped:</td>
                            <td style="font-weight: bold;">{run_data['skipped']}</td>
                        </tr>
                    </table>
                </div>
                
                <p style="color: #a5d1ff; font-size: 14px;">
                    {"Great job! All tests are passing. 🎉" if is_success else "Check the test report (<code>report.html</code>) for detailed failure information."}
                </p>
                
                <hr style="border-color: #003566; margin: 20px 0;">
                <p style="color: #666; font-size: 12px; margin-bottom: 0;">
                    AURA Hotel Test Automation System
                </p>
            </div>
        </body>
        </html>
        """
        
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        msg.attach(part1)
        msg.attach(part2)
        
        # Send via Gmail SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(email_from, email_password)
            server.sendmail(email_from, email_to, msg.as_string())
        
        status = "✅ PASSED" if is_success else "🔴 FAILED"
        print(f"\n[NOTIFICATION] Email sent to {email_to} - Tests {status}")
        return True
        
    except Exception as e:
        print(f"\n[NOTIFICATION] ❌ Failed to send email: {e}")
        return False


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    After pytest finishes, export results to JSON files for the Flask dashboard.
    Also sends email notification with test results.
    """
    results_dir = Path("test_results")
    results_dir.mkdir(exist_ok=True)

    # counts
    total = getattr(terminalreporter, "_numcollected", None)
    passed = len(terminalreporter.stats.get("passed", []))
    failed = len(terminalreporter.stats.get("failed", [])) + len(terminalreporter.stats.get("error", []))
    skipped = len(terminalreporter.stats.get("skipped", []))

    if total is None:
        total = passed + failed + skipped

    run = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "total": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "exitstatus": exitstatus,  # 0 means success
    }

    # write latest
    (results_dir / "latest.json").write_text(json.dumps(run, indent=2), encoding="utf-8")

    # append history
    history_file = results_dir / "history.json"
    if history_file.exists():
        try:
            history = json.loads(history_file.read_text(encoding="utf-8"))
            if not isinstance(history, list):
                history = []
        except Exception:
            history = []
    else:
        history = []

    history.append(run)

    # keep last 30 runs
    history = history[-30:]
    history_file.write_text(json.dumps(history, indent=2), encoding="utf-8")
    
    # === SEND EMAIL NOTIFICATION (for both pass and fail) ===
    send_test_notification(run)


# Now every time you run pytest, those JSON files update automatically.
# An email notification will be sent after every test run (pass or fail).   
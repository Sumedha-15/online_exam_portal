/**
 * Proctoring Engine - Webcam, fullscreen, tab detection, violation logging
 */
class ProctorEngine {
    constructor(attemptId, maxViolations = 5) {
        this.attemptId = attemptId;  // Unique identifier for the exam attempt
        this.maxViolations = maxViolations; // Threshold for auto-submission
        this.violationCount = 0; // Current count of violations
        this.webcamStream = null; // MediaStream object for webcam
        this.isFullscreen = false;
        this.isActive = false;
    }

    async start() { //starts all security measures when exam starts
        this.isActive = true;
        await this.startWebcam(); //start webcam monitoring first to ensure we have access before enforcing fullscreen or other measures
        this.enforceFullscreen();
        this.detectTabSwitch();
        this.preventCopyPaste();
        this.preventRightClick();
        this.updateStatus('Proctoring Active', 'active');
    }

    stop() {
        this.isActive = false;
        if (this.webcamStream) {
            this.webcamStream.getTracks().forEach(t => t.stop());
        }
        document.removeEventListener('visibilitychange', this._visHandler);
        window.removeEventListener('blur', this._blurHandler);
        document.removeEventListener('fullscreenchange', this._fsHandler);
    }

    async startWebcam() {
        const video = document.getElementById('webcamPreview');
        if (!video) return;
        try {
            this.webcamStream = await navigator.mediaDevices.getUserMedia({ //request webcam access with specific constraints
                video: { width: 320, height: 240 }, audio: false // we only need video for proctoring
            });
            video.srcObject = this.webcamStream;
            video.play();
            document.getElementById('webcamStatus').textContent = 'Camera Active';
            document.getElementById('webcamStatus').className = 'status-badge status-active';
        } catch (e) { //if student denies webcam immediately logged as voilation
            this.logViolation('webcam_denied', 'Webcam access was denied');
            document.getElementById('webcamStatus').textContent = 'Camera Denied';
            document.getElementById('webcamStatus').className = 'status-badge status-danger';
        }
    }

    enforceFullscreen() { //enforce fullscreen mode to prevent access to other applications or tabs during the exam
        const el = document.documentElement;
        if (el.requestFullscreen) el.requestFullscreen();
        else if (el.webkitRequestFullscreen) el.webkitRequestFullscreen();
        else if (el.msRequestFullscreen) el.msRequestFullscreen();

        this._fsHandler = () => { //if user exits fullscreen mode log violation and try to re-enter fullscreen after a short delay
            if (!document.fullscreenElement && this.isActive) {
                this.logViolation('fullscreen_exit', 'Exited fullscreen mode');
                setTimeout(() => {
                    if (this.isActive && !document.fullscreenElement) {
                        document.documentElement.requestFullscreen().catch(() => {});
                    }
                }, 1000);
            }
        };
        document.addEventListener('fullscreenchange', this._fsHandler);
    }

    detectTabSwitch() {
        this._visHandler = () => {
            if (document.hidden && this.isActive) { //becomes true when user switches to another tab or minimizes the browser
                this.logViolation('tab_switch', 'Switched to another tab');
            }
        };
        this._blurHandler = () => {
            if (this.isActive) {
                this.logViolation('window_blur', 'Window lost focus'); //fires when user clicks outside the browser window or switches to another application
            }
        };
        document.addEventListener('visibilitychange', this._visHandler);
        window.addEventListener('blur', this._blurHandler);
    }

    preventCopyPaste() {
        document.addEventListener('copy', e => { if (this.isActive) { e.preventDefault(); this.logViolation('copy_attempt', 'Attempted to copy'); }});
        document.addEventListener('paste', e => { if (this.isActive) { e.preventDefault(); this.logViolation('paste_attempt', 'Attempted to paste'); }});
        document.addEventListener('cut', e => { if (this.isActive) { e.preventDefault(); this.logViolation('cut_attempt', 'Attempted to cut'); }});
    }

    preventRightClick() {
        document.addEventListener('contextmenu', e => {
            if (this.isActive) { e.preventDefault(); this.logViolation('right_click', 'Right-click attempted'); }
        });
    }
//every cheat attempt is counted + saved in db + shows warning to student + if max violations reached auto submit the exam after showing final warning
    async logViolation(type, details) {
        this.violationCount++;
        this.updateViolationUI();

        try {
            await fetch('/api/log-violation', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    attempt_id: this.attemptId,
                    violation_type: type,
                    details: details
                })
            });
        } catch (e) {
            console.error('Failed to log violation:', e);
        }

        if (this.violationCount >= this.maxViolations) {
            this.updateStatus('Max Violations Reached!', 'danger');
            showToast('Maximum violations reached! Your exam will be auto-submitted.', 'error');
            setTimeout(() => {
                if (typeof submitExam === 'function') submitExam(true);
            }, 2000);
        }
    }
//updates the violation counter and progress bar in the UI to give real-time feedback to the student about their proctoring status
    updateViolationUI() {
        const counter = document.getElementById('violationCount');
        if (counter) counter.textContent = this.violationCount;
        const bar = document.getElementById('violationBar');
        if (bar) {
            const pct = (this.violationCount / this.maxViolations) * 100;
            bar.style.width = pct + '%';
            bar.className = 'violation-bar-fill' + (pct > 60 ? ' danger' : pct > 30 ? ' warning' : '');
        }
    }

    updateStatus(text, type) {
        const el = document.getElementById('proctorStatus');
        if (el) {
            el.textContent = text;
            el.className = 'status-badge status-' + type;
        }
    }
}


// Show password toggle
document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('password');
    const showPassword = document.getElementById('show-password');
    if (showPassword) {
        showPassword.addEventListener('change', function() {
            passwordInput.type = this.checked ? 'text' : 'password';
        });
    }
});
function evaluatePassword(password) {
    let score = 0;
    let feedback = [];
    let tips = [];
    let hasLength = password.length >= 10;
    let hasUpper = /[A-Z]/.test(password);
    let hasLower = /[a-z]/.test(password);
    let hasNumber = /[0-9]/.test(password);
    let hasSymbol = /[^A-Za-z0-9]/.test(password);
    let commonPattern = /password|1234|qwerty|letmein|admin/i.test(password);

    if (hasLength) score++;
    else tips.push('Use at least 10 characters.');
    if (hasUpper) score++;
    else tips.push('Add uppercase letters.');
    if (hasLower) score++;
    else tips.push('Add lowercase letters.');
    if (hasNumber) score++;
    else tips.push('Add numbers.');
    if (hasSymbol) score++;
    else tips.push('Add special characters.');
    if (commonPattern) {
        score = Math.max(score - 2, 0);
        tips.push('Avoid common words or patterns.');
    }

    let strength = '';
    if (score <= 2) strength = 'Weak';
    else if (score === 3) strength = 'Medium';
    else if (score >= 4 && password.length >= 12) strength = 'Strong';
    else if (score >= 4) strength = 'Medium';

    // Visual indicators
    return {
        strength,
        feedback: tips,
        indicators: { hasLength, hasUpper, hasLower, hasNumber, hasSymbol },
        commonPattern
    };
}

// Small dictionary for demonstration
const DICTIONARY = [
    'password', '1234', 'qwerty', 'letmein', 'admin', 'math', 'welcome', 'test', 'user', 'login', 'abc', 'iloveyou', 'monkey', 'dragon', 'sunshine', 'princess', 'football', 'charlie', 'donald', 'michelle', 'ashley', 'michael', 'jessica', 'daniel', 'david', 'matt', 'sarah', 'alex', 'john', 'emma', 'olivia', 'sophia', 'liam', 'noah', 'lucas', 'jack', 'oliver', 'harry', 'george', 'sam', 'ben', 'max', 'leo', 'oscar', 'mia', 'ava', 'ella', 'grace', 'chloe', 'lily', 'ruby', 'evie', 'freddie', 'archie', 'theo', 'arthur', 'logan', 'james', 'ethan', 'william', 'henry', 'joshua', 'sebastian', 'joseph', 'thomas', 'charlotte', 'amelia', 'isabella', 'sophie', 'emily', 'scarlett', 'mathe', 'maths', 'math0519'
];

function containsDictionaryWord(password) {
    const lower = password.toLowerCase();
    return DICTIONARY.some(word => word.length > 2 && lower.includes(word));
}

// Estimate time to crack password (improved)
function estimateCrackTime(password) {
    // Assume brute force: 10 billion guesses/sec
    const guessesPerSecond = 1e10;
    let charset = 0;
    if (/[a-z]/.test(password)) charset += 26;
    if (/[A-Z]/.test(password)) charset += 26;
    if (/[0-9]/.test(password)) charset += 10;
    if (/[^A-Za-z0-9]/.test(password)) charset += 32; // common symbols
    const totalCombos = Math.pow(charset, password.length);
    let seconds = totalCombos / guessesPerSecond;
    // Penalize if dictionary word is present
    if (containsDictionaryWord(password)) {
        // Assume a dictionary attack can try 1 million passwords/sec
        const dictSeconds = 1 / 1e6; // almost instant
        // If password is only dictionary words and numbers/symbols, make it very fast
        if (/^[A-Za-z0-9@!#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]+$/.test(password)) {
            seconds = Math.min(seconds, dictSeconds * 10);
        } else {
            seconds = Math.min(seconds, 10); // at most 10 seconds
        }
    }
    if (!password) return '';
    if (seconds < 1) return 'Instantly';
    if (seconds < 60) return `${Math.round(seconds)} seconds`;
    if (seconds < 3600) return `${Math.round(seconds/60)} minutes`;
    if (seconds < 86400) return `${Math.round(seconds/3600)} hours`;
    if (seconds < 31536000) return `${Math.round(seconds/86400)} days`;
    if (seconds < 3153600000) return `${Math.round(seconds/31536000)} years`;
    return 'Millions of years';
}

document.getElementById('password').addEventListener('input', function() {
    const password = this.value;
    if (!password) {
        // Reset UI
        document.getElementById('strength').textContent = '';
        document.getElementById('indicator-length').textContent = '🔴 10+ chars';
        document.getElementById('indicator-upper').textContent = '🔴 Uppercase';
        document.getElementById('indicator-lower').textContent = '🔴 Lowercase';
        document.getElementById('indicator-number').textContent = '🔴 Number';
        document.getElementById('indicator-symbol').textContent = '🔴 Symbol';
        document.getElementById('smiley').textContent = '🙂';
        document.getElementById('crack-time').textContent = '';
        document.getElementById('feedback').innerHTML = '';
        document.body.style.background = '#f4f6fb';
        return;
    }
    fetch('http://localhost:5000/api/evaluate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password })
    })
    .then(res => res.json())
    .then(data => {
        const { strength, tips, indicators, commonPattern, crackTime } = data;
        document.getElementById('strength').textContent = `Strength: ${strength}`;
        document.getElementById('indicator-length').textContent = `${indicators.hasLength ? '🟢' : '🔴'} 10+ chars`;
        document.getElementById('indicator-upper').textContent = `${indicators.hasUpper ? '🟢' : '🔴'} Uppercase`;
        document.getElementById('indicator-lower').textContent = `${indicators.hasLower ? '🟢' : '🔴'} Lowercase`;
        document.getElementById('indicator-number').textContent = `${indicators.hasNumber ? '🟢' : '🔴'} Number`;
        document.getElementById('indicator-symbol').textContent = `${indicators.hasSymbol ? '🟢' : '🔴'} Symbol`;
        let smiley = '🙂';
        if (strength === 'Weak') smiley = '😟';
        else if (strength === 'Medium') smiley = '😐';
        else if (strength === 'Strong') smiley = '😃';
        document.getElementById('smiley').textContent = smiley;
        document.getElementById('crack-time').textContent = '';
        let review = '';
        if (strength === 'Weak') {
            review = 'Your password is weak. It can be easily cracked. Try making it longer and using a mix of character types.';
        } else if (strength === 'Medium') {
            review = 'Your password is medium strength. It could be improved by adding more character types and increasing length.';
        } else if (strength === 'Strong') {
            review = 'Great! Your password is strong and hard to crack.';
        }
        if (commonPattern) {
            review += ' Avoid using common words or patterns.';
        }
        document.getElementById('feedback').innerHTML = review + (tips.length ? '<ul>' + tips.map(f => `<li>${f}</li>`).join('') + '</ul>' : '');
        // Change background color based on strength
        if (strength === 'Weak') {
            document.body.style.background = '#ff2222';
        } else if (strength === 'Medium') {
            document.body.style.background = '#ffe600';
        } else if (strength === 'Strong') {
            document.body.style.background = '#00e676';
        }
    })
    .catch(() => {
        document.getElementById('feedback').innerHTML = 'Error: Could not connect to backend.';
    });
});

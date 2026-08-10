import React, { useState } from 'react';
import { registerAPI, loginAPI } from '../services/api';

function AuthView({ onLoginSuccess }) {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [age, setAge] = useState('');
  const [country, setCountry] = useState('');
  const [message, setMessage] = useState('');
  const [step, setStep] = useState('form'); // 'form' or 'check_email'

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    try {
      if (isLogin) {
        const data = await loginAPI(email, password);
        localStorage.setItem('access_token', data.access_token);
        onLoginSuccess();
      } else {
        await registerAPI({ name, email, age: parseInt(age), country, password });
        setStep('check_email');
      }
    } catch (err) {
      setMessage(err.response?.data?.detail || err.message);
    }
  };

  if (step === 'check_email') {
    return (
      <div style={{ maxWidth: 400, margin: '40px auto' }}>
        <h2>Check Your Email</h2>
        <p>We sent an OTP to {email}. Please verify your email before logging in.</p>
        <button onClick={() => { setStep('form'); setIsLogin(true); }}>Back to Login</button>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: 400, margin: '40px auto' }}>
      <h2>{isLogin ? 'Login' : 'Register'}</h2>
      <form onSubmit={handleSubmit}>
        {!isLogin && (
          <>
            <input type="text" placeholder="Full Name" value={name} onChange={(e) => setName(e.target.value)} required />
            <input type="number" placeholder="Age" value={age} onChange={(e) => setAge(e.target.value)} required />
            <input type="text" placeholder="Country" value={country} onChange={(e) => setCountry(e.target.value)} required />
          </>
        )}
        <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        <button type="submit">{isLogin ? 'Login' : 'Register'}</button>
      </form>
      {message && <p style={{ color: 'red' }}>{message}</p>}
      <p>
        {isLogin ? "Don't have an account? " : "Already have an account? "}
        <span style={{ cursor: 'pointer', color: 'blue' }} onClick={() => setIsLogin(!isLogin)}>
          {isLogin ? 'Register' : 'Login'}
        </span>
      </p>
    </div>
  );
}

export default AuthView;
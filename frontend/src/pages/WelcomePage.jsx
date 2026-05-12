import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchCurrentUser, logout } from '../services/auth';
import styles from './WelcomePage.module.css';

export default function WelcomePage() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCurrentUser()
      .then((user) => setUsername(user.username))
      .catch(() => {
        logout();
        navigate('/login');
      })
      .finally(() => setLoading(false));
  }, [navigate]);

  function handleLogout() {
    logout();
    navigate('/login');
  }

  if (loading) {
    return (
      <div className={styles.loadingPage}>
        <div className={styles.loadingSpinner} aria-label="Loading" />
      </div>
    );
  }

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <div className={styles.headerInner}>
          <span className={styles.brand}>Compliance Platform</span>
          <div className={styles.userBar}>
            <span className={styles.userLabel}>{username}</span>
            <button className={styles.logoutBtn} onClick={handleLogout}>
              Sign out
            </button>
          </div>
        </div>
      </header>

      <main className={styles.main}>
        <section className={styles.hero}>
          <div className={styles.gradientShell}>
            <div className={styles.heroCard}>
              <div className={styles.welcomeBadge}>Dashboard</div>
              <h1 className={styles.title}>
                Welcome,{' '}
                <span className={styles.highlight}>{username}</span>
              </h1>
              <p className={styles.description}>
                You are successfully authenticated. This is your compliance
                platform dashboard where you can manage and monitor your
                compliance workflows.
              </p>
            </div>
          </div>
        </section>

        <section className={styles.grid}>
          {CARDS.map((card) => (
            <div key={card.id} className={styles.cardShell}>
              <div className={styles.card}>
                <div className={styles.cardIcon} aria-hidden="true">
                  {card.icon}
                </div>
                <h2 className={styles.cardTitle}>{card.title}</h2>
                <p className={styles.cardDescription}>{card.description}</p>
              </div>
            </div>
          ))}
        </section>
      </main>
    </div>
  );
}

const CARDS = [
  {
    id: 'policies',
    icon: '📋',
    title: 'Policies',
    description:
      "Manage and review your organisation's compliance policies and procedures.",
  },
  {
    id: 'audits',
    icon: '🔍',
    title: 'Audits',
    description:
      'Track ongoing audits and review historical audit reports in one place.',
  },
  {
    id: 'reports',
    icon: '📊',
    title: 'Reports',
    description:
      'Generate and export compliance reports with rich analytical insights.',
  },
  {
    id: 'settings',
    icon: '⚙️',
    title: 'Settings',
    description:
      'Configure platform preferences, user roles, and notification settings.',
  },
];

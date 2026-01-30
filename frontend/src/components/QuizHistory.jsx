import { useState, useEffect } from 'react';
import { getQuizHistory } from '../api/quizApi';

function QuizHistory({ onViewDetails, refreshTrigger }) {
    const [quizzes, setQuizzes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [total, setTotal] = useState(0);

    useEffect(() => {
        fetchHistory();
    }, [refreshTrigger]);

    const fetchHistory = async () => {
        setLoading(true);
        setError('');

        try {
            const data = await getQuizHistory();
            setQuizzes(data.quizzes);
            setTotal(data.total);
        } catch (err) {
            console.error('Error fetching history:', err);
            setError('Failed to load quiz history');
        } finally {
            setLoading(false);
        }
    };

    const formatDate = (dateString) => {
        if (!dateString) return 'N/A';
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
        });
    };

    const truncateUrl = (url, maxLength = 50) => {
        if (url.length <= maxLength) return url;
        return url.substring(0, maxLength) + '...';
    };

    if (loading) {
        return (
            <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
                <div className="spinner" style={{ margin: '0 auto 1rem' }}></div>
                <p>Loading quiz history...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="error-message">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="12" r="10" />
                    <line x1="12" y1="8" x2="12" y2="12" />
                    <line x1="12" y1="16" x2="12.01" y2="16" />
                </svg>
                {error}
                <button className="btn btn-secondary btn-sm" onClick={fetchHistory} style={{ marginLeft: 'auto' }}>
                    Retry
                </button>
            </div>
        );
    }

    if (quizzes.length === 0) {
        return (
            <div className="empty-state">
                <div className="empty-state-icon">
                    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                    </svg>
                </div>
                <h3>No Quizzes Yet</h3>
                <p>Generate your first quiz from the &quot;Generate Quiz&quot; tab!</p>
            </div>
        );
    }

    return (
        <div>
            <div style={{ marginBottom: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <p style={{ color: 'var(--text-secondary)' }}>
                    Showing {quizzes.length} of {total} quizzes
                </p>
                <button className="btn btn-secondary btn-sm" onClick={fetchHistory}>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <polyline points="1 4 1 10 7 10" />
                        <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10" />
                    </svg>
                    Refresh
                </button>
            </div>

            <div className="history-table-container">
                <table className="history-table">
                    <thead>
                        <tr>
                            <th>Title</th>
                            <th>URL</th>
                            <th>Questions</th>
                            <th>Created</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {quizzes.map((quiz) => (
                            <tr key={quiz.id}>
                                <td className="table-title">{quiz.title}</td>
                                <td className="table-url" title={quiz.url}>
                                    <a href={quiz.url} target="_blank" rel="noopener noreferrer">
                                        {truncateUrl(quiz.url)}
                                    </a>
                                </td>
                                <td>
                                    <span className="meta-badge" style={{ display: 'inline-flex' }}>
                                        {quiz.question_count} Q
                                    </span>
                                </td>
                                <td className="table-date">{formatDate(quiz.created_at)}</td>
                                <td>
                                    <button
                                        className="btn btn-secondary btn-sm"
                                        onClick={() => onViewDetails(quiz.id)}
                                    >
                                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                                            <circle cx="12" cy="12" r="3" />
                                        </svg>
                                        Details
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default QuizHistory;

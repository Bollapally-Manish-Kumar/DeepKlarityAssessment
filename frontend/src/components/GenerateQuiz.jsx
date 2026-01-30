import { useState } from 'react';
import { generateQuiz } from '../api/quizApi';
import QuizDisplay from './QuizDisplay';

function GenerateQuiz({ onQuizGenerated }) {
    const [url, setUrl] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [quiz, setQuiz] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!url.trim()) {
            setError('Please enter a Wikipedia URL');
            return;
        }

        // Validate Wikipedia URL
        if (!url.includes('wikipedia.org/wiki/')) {
            setError('Please enter a valid Wikipedia article URL');
            return;
        }

        setLoading(true);
        setError('');
        setQuiz(null);

        try {
            const result = await generateQuiz(url.trim());
            setQuiz(result);
            onQuizGenerated?.();
        } catch (err) {
            console.error('Error generating quiz:', err);
            setError(
                err.response?.data?.detail ||
                'Failed to generate quiz. Please try again.'
            );
        } finally {
            setLoading(false);
        }
    };

    const handleExampleClick = (exampleUrl) => {
        setUrl(exampleUrl);
    };

    return (
        <div>
            {/* URL Input Form */}
            <form onSubmit={handleSubmit}>
                <div className="input-group">
                    <input
                        type="url"
                        className="url-input"
                        placeholder="Enter a Wikipedia article URL (e.g., https://en.wikipedia.org/wiki/Alan_Turing)"
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                        disabled={loading}
                    />
                    <button
                        type="submit"
                        className="btn btn-primary"
                        disabled={loading}
                    >
                        {loading ? (
                            <>
                                <span className="spinner"></span>
                                Generating...
                            </>
                        ) : (
                            <>
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <circle cx="12" cy="12" r="10" />
                                    <circle cx="12" cy="12" r="3" />
                                    <line x1="12" y1="2" x2="12" y2="4" />
                                    <line x1="12" y1="20" x2="12" y2="22" />
                                    <line x1="2" y1="12" x2="4" y2="12" />
                                    <line x1="20" y1="12" x2="22" y2="12" />
                                </svg>
                                Generate Quiz
                            </>
                        )}
                    </button>
                </div>
            </form>

            {/* Example URLs */}
            {!quiz && !loading && (
                <div style={{ marginBottom: '2rem' }}>
                    <p style={{ marginBottom: '0.75rem', color: 'var(--text-muted)' }}>
                        Try these examples:
                    </p>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                        {[
                            { title: 'Alan Turing', url: 'https://en.wikipedia.org/wiki/Alan_Turing' },
                            { title: 'World War II', url: 'https://en.wikipedia.org/wiki/World_War_II' },
                            { title: 'Artificial Intelligence', url: 'https://en.wikipedia.org/wiki/Artificial_intelligence' },
                            { title: 'Albert Einstein', url: 'https://en.wikipedia.org/wiki/Albert_Einstein' },
                        ].map((example) => (
                            <button
                                key={example.url}
                                className="topic-tag"
                                onClick={() => handleExampleClick(example.url)}
                                type="button"
                            >
                                {example.title}
                            </button>
                        ))}
                    </div>
                </div>
            )}

            {/* Error Message */}
            {error && (
                <div className="error-message">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <circle cx="12" cy="12" r="10" />
                        <line x1="12" y1="8" x2="12" y2="12" />
                        <line x1="12" y1="16" x2="12.01" y2="16" />
                    </svg>
                    {error}
                </div>
            )}

            {/* Loading State */}
            {loading && (
                <div className="card loading-card">
                    <div className="loading-animation">
                        <div className="loading-circle"></div>
                        <div className="loading-circle"></div>
                        <div className="loading-circle"></div>
                    </div>
                    <h3 style={{ marginBottom: '0.5rem' }}>Generating Your Quiz</h3>
                    <p>Scraping article and creating questions with AI...</p>
                    <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginTop: '1rem' }}>
                        This may take 15-30 seconds
                    </p>
                </div>
            )}

            {/* Quiz Display */}
            {quiz && !loading && (
                <QuizDisplay quiz={quiz} showTakeQuizMode={true} />
            )}
        </div>
    );
}

export default GenerateQuiz;

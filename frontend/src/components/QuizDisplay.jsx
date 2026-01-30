import { useState } from 'react';

function QuizDisplay({ quiz, showTakeQuizMode = false }) {
    const [mode, setMode] = useState('review'); // 'review' or 'take'
    const [selectedAnswers, setSelectedAnswers] = useState({});
    const [submitted, setSubmitted] = useState(false);

    const handleOptionSelect = (questionIndex, option) => {
        if (submitted) return;
        setSelectedAnswers((prev) => ({
            ...prev,
            [questionIndex]: option,
        }));
    };

    const handleSubmitQuiz = () => {
        setSubmitted(true);
    };

    const handleResetQuiz = () => {
        setSelectedAnswers({});
        setSubmitted(false);
    };

    const calculateScore = () => {
        if (!quiz?.quiz) return { correct: 0, total: 0 };
        let correct = 0;
        quiz.quiz.forEach((q, index) => {
            if (selectedAnswers[index] === q.answer) {
                correct++;
            }
        });
        return { correct, total: quiz.quiz.length };
    };

    const score = calculateScore();
    const isReviewMode = mode === 'review';

    const getScoreMessage = () => {
        if (score.correct === score.total) return 'Perfect Score!';
        if (score.correct >= score.total * 0.7) return 'Great Job!';
        if (score.correct >= score.total * 0.5) return 'Good Effort!';
        return 'Keep Learning!';
    };

    return (
        <div>
            {/* Quiz Header */}
            <div className="quiz-header">
                <h2 className="quiz-title">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
                        <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
                    </svg>
                    <a href={quiz.url} target="_blank" rel="noopener noreferrer">
                        {quiz.title}
                    </a>
                </h2>

                <div className="quiz-meta">
                    <span className="meta-badge">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <circle cx="12" cy="12" r="10" />
                            <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" />
                            <line x1="12" y1="17" x2="12.01" y2="17" />
                        </svg>
                        {quiz.quiz?.length || 0} Questions
                    </span>
                    {quiz.created_at && (
                        <span className="meta-badge">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
                                <line x1="16" y1="2" x2="16" y2="6" />
                                <line x1="8" y1="2" x2="8" y2="6" />
                                <line x1="3" y1="10" x2="21" y2="10" />
                            </svg>
                            {new Date(quiz.created_at).toLocaleDateString()}
                        </span>
                    )}
                </div>

                {quiz.summary && (
                    <p className="quiz-summary">{quiz.summary}</p>
                )}
            </div>

            {/* Key Entities */}
            {quiz.key_entities && (
                <div style={{ marginBottom: '2rem' }}>
                    <h3 className="section-title">Key Entities</h3>
                    <div className="entities-grid">
                        {quiz.key_entities.people?.length > 0 && (
                            <div className="entity-card">
                                <div className="entity-title">
                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                                        <circle cx="12" cy="7" r="4" />
                                    </svg>
                                    People
                                </div>
                                <div className="entity-list">
                                    {quiz.key_entities.people.map((person, i) => (
                                        <span key={i} className="entity-item">{person}</span>
                                    ))}
                                </div>
                            </div>
                        )}
                        {quiz.key_entities.organizations?.length > 0 && (
                            <div className="entity-card">
                                <div className="entity-title">
                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
                                        <polyline points="9 22 9 12 15 12 15 22" />
                                    </svg>
                                    Organizations
                                </div>
                                <div className="entity-list">
                                    {quiz.key_entities.organizations.map((org, i) => (
                                        <span key={i} className="entity-item">{org}</span>
                                    ))}
                                </div>
                            </div>
                        )}
                        {quiz.key_entities.locations?.length > 0 && (
                            <div className="entity-card">
                                <div className="entity-title">
                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                        <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
                                        <circle cx="12" cy="10" r="3" />
                                    </svg>
                                    Locations
                                </div>
                                <div className="entity-list">
                                    {quiz.key_entities.locations.map((loc, i) => (
                                        <span key={i} className="entity-item">{loc}</span>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* Sections */}
            {quiz.sections?.length > 0 && (
                <div style={{ marginBottom: '2rem' }}>
                    <h3 className="section-title">Article Sections</h3>
                    <div className="sections-list">
                        {quiz.sections.map((section, i) => (
                            <span key={i} className="section-tag">{section}</span>
                        ))}
                    </div>
                </div>
            )}

            {/* Quiz Mode Toggle */}
            {showTakeQuizMode && quiz.quiz?.length > 0 && (
                <div className="quiz-mode-toggle">
                    <button
                        className={`btn btn-secondary ${isReviewMode ? 'active' : ''}`}
                        onClick={() => { setMode('review'); handleResetQuiz(); }}
                    >
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
                            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
                        </svg>
                        Review Mode
                    </button>
                    <button
                        className={`btn btn-secondary ${!isReviewMode ? 'active' : ''}`}
                        onClick={() => { setMode('take'); handleResetQuiz(); }}
                    >
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <polygon points="5 3 19 12 5 21 5 3" />
                        </svg>
                        Take Quiz
                    </button>
                </div>
            )}

            {/* Questions */}
            <h3 className="section-title">Quiz Questions</h3>
            <div className="questions-grid">
                {quiz.quiz?.map((question, index) => (
                    <div key={index} className="question-card">
                        <span className="question-number">Q{index + 1}</span>

                        <div className="question-header">
                            <span className="question-text">{question.question}</span>
                            <span className={`difficulty-badge difficulty-${question.difficulty}`}>
                                {question.difficulty}
                            </span>
                        </div>

                        <div className="options-list">
                            {question.options.map((option, optIndex) => {
                                const letter = String.fromCharCode(65 + optIndex);
                                const isCorrect = option === question.answer;
                                const isSelected = selectedAnswers[index] === option;

                                let className = 'option-item';
                                if (!isReviewMode) {
                                    if (submitted) {
                                        if (isCorrect) className += ' correct';
                                        else if (isSelected && !isCorrect) className += ' incorrect';
                                    } else if (isSelected) {
                                        className += ' selected';
                                    }
                                } else if (isCorrect) {
                                    className += ' correct';
                                }

                                return (
                                    <div
                                        key={optIndex}
                                        className={className}
                                        onClick={() => !isReviewMode && handleOptionSelect(index, option)}
                                        style={{ cursor: isReviewMode ? 'default' : 'pointer' }}
                                    >
                                        <span className="option-letter">{letter}</span>
                                        <span className="option-text">{option}</span>
                                        {isReviewMode && isCorrect && (
                                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" className="check-icon">
                                                <polyline points="20 6 9 17 4 12" />
                                            </svg>
                                        )}
                                        {!isReviewMode && submitted && isCorrect && (
                                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" className="check-icon">
                                                <polyline points="20 6 9 17 4 12" />
                                            </svg>
                                        )}
                                        {!isReviewMode && submitted && isSelected && !isCorrect && (
                                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" className="x-icon">
                                                <line x1="18" y1="6" x2="6" y2="18" />
                                                <line x1="6" y1="6" x2="18" y2="18" />
                                            </svg>
                                        )}
                                    </div>
                                );
                            })}
                        </div>

                        {/* Answer Section - Show in review mode or after submission */}
                        {(isReviewMode || submitted) && (
                            <div className="answer-section">
                                <div className="answer-label">Answer</div>
                                <div className="answer-text">{question.answer}</div>
                                <div className="explanation-text">{question.explanation}</div>
                            </div>
                        )}
                    </div>
                ))}
            </div>

            {/* Submit Button for Take Quiz Mode */}
            {!isReviewMode && !submitted && quiz.quiz?.length > 0 && (
                <div style={{ textAlign: 'center', marginTop: '2rem' }}>
                    <button
                        className="btn btn-primary"
                        onClick={handleSubmitQuiz}
                        disabled={Object.keys(selectedAnswers).length < quiz.quiz.length}
                    >
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <polyline points="20 6 9 17 4 12" />
                        </svg>
                        Submit Quiz ({Object.keys(selectedAnswers).length}/{quiz.quiz.length} answered)
                    </button>
                </div>
            )}

            {/* Score Display */}
            {!isReviewMode && submitted && (
                <div className="quiz-score">
                    <div className="score-value">
                        {score.correct}/{score.total}
                    </div>
                    <div className="score-label">
                        {getScoreMessage()}
                    </div>
                    <button
                        className="btn btn-secondary"
                        onClick={handleResetQuiz}
                        style={{ marginTop: '1rem' }}
                    >
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <polyline points="1 4 1 10 7 10" />
                            <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10" />
                        </svg>
                        Try Again
                    </button>
                </div>
            )}

            {/* Related Topics */}
            {quiz.related_topics?.length > 0 && (
                <div style={{ marginTop: '2rem' }}>
                    <h3 className="section-title">Related Topics</h3>
                    <div className="related-topics">
                        {quiz.related_topics.map((topic, i) => (
                            <a
                                key={i}
                                className="topic-tag"
                                href={`https://en.wikipedia.org/wiki/${encodeURIComponent(topic.replace(/ /g, '_'))}`}
                                target="_blank"
                                rel="noopener noreferrer"
                            >
                                {topic}
                            </a>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}

export default QuizDisplay;

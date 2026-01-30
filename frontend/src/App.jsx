import { useState, useEffect } from 'react';
import GenerateQuiz from './components/GenerateQuiz';
import QuizHistory from './components/QuizHistory';
import QuizModal from './components/QuizModal';
import { getQuizDetails } from './api/quizApi';

function App() {
    const [activeTab, setActiveTab] = useState('generate');
    const [modalQuiz, setModalQuiz] = useState(null);
    const [refreshHistory, setRefreshHistory] = useState(0);

    const handleViewDetails = async (quizId) => {
        try {
            const quiz = await getQuizDetails(quizId);
            setModalQuiz(quiz);
        } catch (error) {
            console.error('Error fetching quiz details:', error);
            alert('Failed to load quiz details');
        }
    };

    const handleQuizGenerated = () => {
        // Trigger history refresh when a new quiz is generated
        setRefreshHistory((prev) => prev + 1);
    };

    return (
        <div className="app-container">
            {/* Header */}
            <header className="app-header">
                <h1>
                    <span className="logo-icon">
                        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="url(#gradient)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                            <path d="M2 17L12 22L22 17" stroke="url(#gradient)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                            <path d="M2 12L12 17L22 12" stroke="url(#gradient)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                            <defs>
                                <linearGradient id="gradient" x1="2" y1="2" x2="22" y2="22">
                                    <stop stopColor="#6366f1" />
                                    <stop offset="1" stopColor="#8b5cf6" />
                                </linearGradient>
                            </defs>
                        </svg>
                    </span>
                    Wiki Quiz
                </h1>
                <p>Generate AI-powered quizzes from any Wikipedia article</p>
            </header>

            {/* Tab Navigation */}
            <nav className="tab-navigation">
                <button
                    className={`tab-button ${activeTab === 'generate' ? 'active' : ''}`}
                    onClick={() => setActiveTab('generate')}
                >
                    <span className="tab-icon">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
                        </svg>
                    </span>
                    Generate Quiz
                </button>
                <button
                    className={`tab-button ${activeTab === 'history' ? 'active' : ''}`}
                    onClick={() => setActiveTab('history')}
                >
                    <span className="tab-icon">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                            <polyline points="14 2 14 8 20 8" />
                            <line x1="16" y1="13" x2="8" y2="13" />
                            <line x1="16" y1="17" x2="8" y2="17" />
                            <polyline points="10 9 9 9 8 9" />
                        </svg>
                    </span>
                    Past Quizzes
                </button>
            </nav>

            {/* Tab Content */}
            <main>
                {activeTab === 'generate' && (
                    <GenerateQuiz onQuizGenerated={handleQuizGenerated} />
                )}
                {activeTab === 'history' && (
                    <QuizHistory
                        onViewDetails={handleViewDetails}
                        refreshTrigger={refreshHistory}
                    />
                )}
            </main>

            {/* Modal */}
            {modalQuiz && (
                <QuizModal quiz={modalQuiz} onClose={() => setModalQuiz(null)} />
            )}
        </div>
    );
}

export default App;

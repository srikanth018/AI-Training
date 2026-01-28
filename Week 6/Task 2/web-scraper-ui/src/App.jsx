import { useState } from 'react'
import './App.css'
import ChatInterface from './components/ChatInterface'

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>🤖 Bedrock AI Web Scraper</h1>
        <p>Ask questions and get web-scraped content from AWS Lambda</p>
      </header>
      <ChatInterface />
    </div>
  )
}

export default App

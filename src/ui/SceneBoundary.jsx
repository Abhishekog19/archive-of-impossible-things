import { Component } from 'react'

/** Catch boot asset/render failures outside Canvas so recovery remains usable. */
export default class SceneBoundary extends Component {
  state = { failed: false }

  static getDerivedStateFromError() { return { failed: true } }

  render() {
    if (this.state.failed) return <main className="fallback" role="alert">
      <h1>The Archive couldn’t open</h1>
      <p>Some scenery couldn’t load. Check your connection and try again.</p>
      <button className="scene-retry" onClick={() => window.location.reload()}>Reload environment</button>
    </main>
    return this.props.children
  }
}

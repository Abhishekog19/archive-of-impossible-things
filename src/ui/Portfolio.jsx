import { useEffect } from 'react'
import profile from '../content/portfolio.json'
import '../story/story.css'

export default function Portfolio() {
  useEffect(() => {
    document.title = `${profile.name} — Developer & Explorer`
    document.getElementById(window.location.hash.slice(1))?.scrollIntoView()
  }, [])
  return <main className="portfolio">
    <nav aria-label="Portfolio navigation"><a href="?">The Archive</a><div><a href="#work">Selected work</a><a href="?chapter=spring&start=forest">Try the story experiment ↗</a></div></nav>
    <header><p className="portfolio-eyebrow">A curiosity for what comes next</p><h1>{profile.name}<span>Ideas, explored.<br/>Things, built.</span></h1><p className="portfolio-intro">Electronics and Telecommunication Engineering student, full-stack developer, and technology enthusiast.</p><p>{profile.introduction} {profile.statement}</p></header>
    <section aria-labelledby="skills-title"><p className="portfolio-eyebrow">01 / Tools for exploration</p><h2 id="skills-title">Across disciplines.</h2><ul className="portfolio-skills">{profile.skills.map(skill => <li key={skill.name}><strong>{skill.name}</strong>{skill.technologies.length > 0 && <span>{skill.technologies.join(' · ')}</span>}</li>)}</ul></section>
    <section id="work" aria-labelledby="work-title"><p className="portfolio-eyebrow">02 / Selected work</p><h2 id="work-title">Different questions.<br/>Working products.</h2>{profile.projects.map((p,i) => <article key={p.id} id={p.id}><span className="portfolio-number">0{i+1}</span><div><h3>{p.title}</h3><p>{p.description}</p></div></article>)}</section>
    <footer><p className="portfolio-eyebrow">Still exploring</p><h2>Curiosity is the common thread.</h2><p>For recruiters, fellow developers, and potential collaborators: welcome to my corner of the web.</p><a href="?chapter=spring&start=forest">Step into the Archive ↗</a></footer>
  </main>
}

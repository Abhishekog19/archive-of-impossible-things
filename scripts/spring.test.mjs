import test from 'node:test'
import assert from 'node:assert/strict'
import { directSpring, EMPTY_SPRING, readSpring } from '../src/story/spring.js'

test('root discovery requires both lessons, in either order', () => {
  for (const routes of [['leaves','stones'],['stones','leaves']]) {
    let state = directSpring({...EMPTY_SPRING},'root')
    assert.equal(state.complete,false)
    state = directSpring(state,routes[0])
    state = directSpring(state,'root')
    assert.equal(state.complete,false)
    state = directSpring(state,routes[1])
    assert.equal(state.complete,false)
    state = directSpring(state,'root')
    assert.equal(state.complete,true)
    assert.equal(directSpring(state,'leaves').complete,true)
  }
})
test('repeat choices do not manufacture the missing lesson', () => {
  let state = {...EMPTY_SPRING}
  for(let i=0;i<10;i++) state=directSpring(state,'leaves')
  assert.equal(directSpring(state,'root').complete,false)
  assert.equal(directSpring(state,'invalid'),state)
})
test('reload preserves valid progress without replaying an interaction', () => {
  const saved = {version:1,bent:true,lifted:true,complete:true,route:'root'}
  assert.deepEqual(readSpring(JSON.stringify(saved)),{bent:true,lifted:true,complete:true,route:null})
  assert.equal(readSpring(JSON.stringify({...saved,lifted:false})).complete,false)
  for(const raw of ['invalid','null','{}','{"version":2}',null]) assert.deepEqual(readSpring(raw),EMPTY_SPRING)
})

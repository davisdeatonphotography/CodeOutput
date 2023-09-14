const { send, receive } = window.api;

document.getElementById('analyze-button').addEventListener('click', async () => {
  const directory = document.getElementById('directory-input').value;
  const openaiKey = document.getElementById('openai-key-input').value;

  send('analyze', { directory, openaiKey });
});

receive('analysis-result', (result) => {
  document.getElementById('output').innerText = result;
});
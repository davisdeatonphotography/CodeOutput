const { app, BrowserWindow, ipcMain } = require('electron');
const { PythonShell } = require('python-shell');
const path = require('path');

function createWindow () {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  mainWindow.loadFile('index.html');
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
});

ipcMain.on('analyze', (event, { directory, openaiKey }) => {
  let options = {
    scriptPath : path.join(__dirname, '..'),
    args: [directory, openaiKey]
  };

  PythonShell.run('electron_bridge.py', options, (err, results) => {
    if (err) throw err;
    // Send the results back to the renderer process
    event.reply('analysis-result', JSON.parse(results[0]));
  });
});
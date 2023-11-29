import express from 'express'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

const app = express();

app.use(express.static(path.join(__dirname, '..', '..', 'public')))

// for testing
app.get('/api/getList', (req, res) => {
    var list = ["item1", "item2", "item3"]
    res.json(list)
    console.log('Sent list of items')
})

app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '..', '..', 'public', 'index.html'))
})

const port = process.env.PORT || 3000;
app.listen(port, () => {
    console.log(`Running: http://localhost:${port}`)
})

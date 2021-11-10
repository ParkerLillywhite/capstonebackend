

const express = require('express')
const app = express()
 
app.use(express.static('public'))

app.get('/app', function (req, res) {
    res.header("Access-Control-Allow-Origin", "*");
    
})
 
app.listen(3000, () => {
    console.log('alive');
})
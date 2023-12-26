document.addEventListener("DOMContentLoaded", function(event) {
    let current_number = document.getElementById('current_number');
    let current_description = document.getElementById('current_description');
    let coming_up = document.getElementById('coming_up');
    let increment = undefined;
    let updateNumber = function(json) {
        console.log(json);
        if (increment !== undefined) {
            clearInterval(increment);
        }
        current_number.innerText = json.number.now;
        current_number.style.color = "rgb(" + json.number.color.r + "," + json.number.color.g + "," + json.number.color.b + ")";
        current_description.innerText = json.number.description;
        let length = json.number.description.length;

        if (length > 100) {
            current_description.style.fontSize = '0.5em';
        } else if (length > 50) {
            current_description.style.fontSize = '0.8em';
        }

        coming_up.innerHTML = '';
        for (n of json.coming_up) {
            let li = document.createElement('li');
            li.append(document.createTextNode(n.description + ': '))
            let li_n = document.createElement('span');
            li_n.innerText = n.initial;
            li_n.style.color = "rgb(" + n.color.r + "," + n.color.g + "," + n.color.b + ")";
            li.append(li_n);
            coming_up.append(li);
        }

        let initial = Number(json.number.now)
        if (isNaN(initial)) {
            increment = undefined;
        } else {
            let start = Date.now();
            increment = setInterval(function () {
                let n = Math.floor(initial + (Date.now() - start) * json.number.increment / 1000);
                current_number.innerText = "" + n;
            }, 100);
        }
    }
    let updateStatsWs = function() {
    let url = (location.protocol == 'https:' ? 'wss' : 'ws')
      + '://' + location.host + location.pathname + 'ws'
    ws = new WebSocket(url);
    ws.onopen = function(e) {
      //updateConnected(true);
    }
    ws.onmessage = function(e) {
      let json = JSON.parse(e.data)
      updateNumber(json);
    }
    ws.onclose = function(e) {
      //updateConnected(false);
      setTimeout(updateStatsWs, 10000);
    }
  }

  //setInterval(updateStats, 100);
  updateStatsWs();
});
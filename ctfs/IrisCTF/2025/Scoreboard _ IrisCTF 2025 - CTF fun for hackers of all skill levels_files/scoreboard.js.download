function timestampToPoint(timestamp) {
    return new Date(timestamp * 1000);
}

async function updateCharts() {
    let data = await (await fetch("/api?get=scoreboard_detail")).json();

    let scores = data.scores.sort((a, b) => (a.added - b.added));
    let users = data.users.reduce((map, obj) => (map[obj.user_id] = obj, map), {});
    let usersList = data.users;

    let datasets = [];
    let uidToDataset = {};
    for(let user of Object.values(users)) {
        let dataset = {label: user.team, team: user.team, data: [{x: window.ctfStart, y: 0}]};
        datasets.push(dataset);
        uidToDataset[user.user_id] = dataset;
    }

    let lasts = {};
    for(let submission of scores) {
        uidToDataset[submission.user_id].data.push(
            {x: timestampToPoint(submission.added), y: submission.points}
        );
        lasts[submission.user_id] = submission.points;
    }

    for(let i = 0; i < usersList.length; i++) {
        datasets[i].data.push(
            {x: new Date(), y: lasts[usersList[i].user_id]}
        );
    }

    window.graph.data.datasets = datasets;
    window.graph.update();
}

async function ready() {
    let graph = document.getElementById("graph");
    let ctx = document.createElement("canvas");
    ctx.style = "filter: invert(1) hue-rotate(180deg); max-width: 100%; max-height: 40vh;";
    let locale = dateFns.locale.enUS;
    let lStr = navigator.language.replace("_", "");
    if(lStr in dateFns.locale) {
        locale = dateFns.locale[lStr];
    }

    window.graph = new Chart(ctx, {
        type: 'line',
        data: {datasets: []},
        options: {
          responsive: true,
          plugins: {
            title: {
              text: 'Scoreboard Top 10',
              display: false
            }
          },
          scales: {
            x: {
              type: 'time',
              adapters: {date: {locale: locale}},
              time: {
                tooltipFormat: 'PPpp'
              },
              title: {
                display: true,
                text: 'Date'
              }
            },
            y: {
              title: {
                display: true,
                text: 'Score'
              }
            }
          },
        },
    });

    graph.appendChild(ctx);
    graph.style = "display: flex;";
    
    let startResp = await fetch("/api?get=start_time");
    let startJson = await startResp.json();
    let start = startJson["time"];
    window.ctfStart = timestampToPoint(start);
    await updateCharts();

    setInterval(updateCharts, 5 * 60 * 1000); // Update scoreboard chart every 5 minutes.
}

document.addEventListener("DOMContentLoaded", ready);

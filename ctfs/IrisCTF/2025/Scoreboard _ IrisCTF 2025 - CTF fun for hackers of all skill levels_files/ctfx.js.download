function addSFX() {
    var btn_dynamic_mouseover = document.getElementById("audio-btn-dynamic-mouseover");
    var btn_dynamic_click = document.getElementById("audio-btn-dynamic-click");

    var btn_solid_mouseover = document.getElementById("audio-btn-solid-mouseover");
    var btn_solid_click = document.getElementById("audio-btn-solid-click");

    var nav_mouseover = document.getElementById("audio-nav-mouseover");
    var nav_click = document.getElementById("audio-nav-click");

    var checkbox_click = document.getElementById("audio-checkbox-click");

    document.querySelectorAll('.btn-dynamic').forEach((e) => {
        e.addEventListener('mouseenter', function() { btn_dynamic_mouseover.currentTime = 0; btn_dynamic_mouseover.play(); });
        e.addEventListener('mouseout', function() { btn_dynamic_mouseover.pause(); });
        e.addEventListener('click', function() { btn_dynamic_click.currentTime = 0; btn_dynamic_click.play(); });
    });

    document.querySelectorAll('.btn-solid:not(.active):not(.btn-solid-link)').forEach((e) => {
        e.addEventListener('mouseenter', function() { btn_solid_mouseover.currentTime = 0; btn_solid_mouseover.play(); });
        e.addEventListener('mouseout', function() { btn_solid_mouseover.pause(); });
        e.addEventListener('click', function() { btn_solid_click.currentTime = 0; btn_solid_click.play(); });
    });

    document.querySelectorAll('.btn-solid-link:not(.active):not(.btn-solid-link-unclickable), #navbar-buttons a, #navbar-buttons button').forEach((e) => {
        e.addEventListener('mouseenter', function() { btn_solid_mouseover.currentTime = 0; nav_mouseover.play(); });
        e.addEventListener('mouseout', function() { nav_mouseover.pause(); });
        e.addEventListener('click', function() { nav_click.currentTime = 0; nav_click.play(); });
    });

    document.querySelectorAll('.container-checkbox').forEach((e) => {
        e.addEventListener('click', function() { checkbox_click.currentTime = 0; checkbox_click.play(); });
    });
}

function typeWriterSFX() {
    var t = document.getElementsByClassName("typewriter")[0],
        e = document.getElementById("audio-typewriter");
    null != t && (e.play(), setTimeout(function() {
        e.pause()
    }, 300 + 1000 / 65 * t.innerText.length))
}

function init_countdowns() {
    var countdowns = document.querySelectorAll(".countdown");

    setInterval(function() {
        for (countdown of countdowns) {
            var new_time = parseInt(countdown.attributes["time-difference"].value);
            if (new_time != 0) new_time -= 1;

            var approx_fun = (new_time > 0) ? Math.floor : Math.ceil;

            var seconds = Math.abs(new_time % 60);
            var minutes = Math.abs(approx_fun(new_time / 60) % 60);
            var hours = Math.abs(approx_fun(new_time / (60 * 60)) % 24);
            var days = Math.abs(approx_fun(new_time / (60 * 60 * 24)));

            var new_inner_text = "";
            if (days) new_inner_text = days + " Day" + (days==1?"":"s") + ", " + hours + " Hour" + (hours==1?"":"s");
            else if (hours) new_inner_text = hours + " Hour" + (hours==1?"":"s") + ", " + minutes + " Minute" + (minutes==1?"":"s");
            else if (minutes) new_inner_text = minutes + " Minute" + (minutes==1?"":"s") + ", " + seconds + " Second" + (seconds==1?"":"s");
            else new_inner_text = seconds + " Second" + (seconds==1?"":"s");

            // Lazy update
            if (new_inner_text != countdown.innerText) countdown.innerText = new_inner_text;
            countdown.attributes["time-difference"].value = new_time;
        }
    }, 1000);
}

const shortTimeFormat = new Intl.DateTimeFormat(undefined, { dateStyle: undefined, timeStyle: "short"});
const longTimeFormat = new Intl.DateTimeFormat(undefined, { dateStyle: "short", timeStyle: "medium"});

function update_news_bar() {
    var news = document.getElementById("news-bar");
    async function update_news_bar_() {
        let news_data = await fetch("/api?get=news");
        news_data = await news_data.json();

        if (news_data.length > 0) {
            // Parse news
            let new_inner_text = "News (click for details): ";
            for (let item of news_data) {
                let date = new Date(item["added"] * 1000);
                new_inner_text += `[${shortTimeFormat.format(date)}] ${item["title"]} `;
            }
            if (new_inner_text != news.innerText) news.innerText = new_inner_text;
        } else news.innerText = "No news yet!";
    }

    setInterval(update_news_bar_, 1000 * 60 * 5);
    update_news_bar_();
}

const newsItems = document.getElementsByClassName("datetime");
if (newsItems.length > 0) {
    for (let t of newsItems) {
        let date = new Date(Number(t.innerText) * 1000);
        t.innerText = longTimeFormat.format(date);
    }
}

update_news_bar();
init_countdowns();
typeWriterSFX();
addSFX();
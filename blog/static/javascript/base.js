document.addEventListener('DOMContentLoaded', function () {

    var instance = M.Tabs.init(document.querySelectorAll('.tabs'), { "onShow": load_page });

    

    document.querySelectorAll('.tab-link').forEach(element => {
        element.onclick = function () {
            console.log(element.id)
            load_page(element.id)
        }
    });
    // Start by loading first page.
    load_page('blog');
    

});

// Renders contents of new page in main view.
function load_page(id) {

    const request = new XMLHttpRequest();
    request.open('GET', id);
    request.onload = () => {
        const response = request.responseText;
        const data = JSON.parse(request.responseText);

        // Push state to URL.
        document.title = id;
        //history.pushState({'title': id, 'text': response, 'tabID':id}, id, id);
        if (id == "blog") {
            document.querySelector('.content').innerHTML = "";
            const template = Handlebars.compile(document.querySelector('#blog_post').innerHTML);
            for (i = 0; i < data.posts.length; i++) {
                const post = data.posts[i];
                const content = template({ "title": post.title, "author": post.author, "date": post.date, "content": post.content });
                document.querySelector('.content').innerHTML += content;
            }
            document.querySelectorAll('.post').forEach(function (element) {
                element.classList.remove("hideit");
                element.classList.add("showit");
            })
        }
        else if (id == "portfolio") {
            document.querySelectorAll('.post').forEach(function (element) {
                //element.style.animationPlayState = 'running';
                element.classList.remove("showit");
                element.classList.add("hideit");
                element.addEventListener('animationend', () => {
                    if (element.classList.contains("hideit")) {
                        document.querySelector('.content').innerHTML = "";
                        const template = Handlebars.compile(document.querySelector('#project_post').innerHTML);
                        for (i = 0; i < data.projects.length; i++) {
                            const project = data.projects[i];
                            const content = template({ "title": project.title, "link": project.link, "content": project.description });
                            document.querySelector('.content').innerHTML += content;
                        }

                        document.querySelectorAll('.post').forEach(function (element) {
                            element.classList.remove("hideit");
                            element.classList.add("showit");
                        })
                    }
                });
            })
        }
    };
    request.send();

}

// Update text on popping state.
window.onpopstate = e => {
    const data = e.state;
    document.title = data.title;
    var instance = M.Tabs.getInstance(document.querySelectorAll('.tabs'));
    instance.select('#' + data.tabID)
    //document.querySelector('#'+data.tabID).select()
    document.querySelector('.content').innerHTML = data.text;
};
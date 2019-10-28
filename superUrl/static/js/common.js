var index = {};
index.index = {
    html: function () {
        var HTML = '<div id="top">';
        HTML += '<div class="not-login" style="display: inline-block;">';
        HTML += '<a href="/v1/user/register">注册</a>';
        HTML += '<a href="/v1/user/login">登陆</a>';
        HTML += '</div>';
        HTML += '<div class="login" style="display: inline-block;">';
        HTML += '<form action="" method="post" enctype="multipart/form-data" id="avatar_form" style="display: none;">';
        HTML += '<input type="file" name="fileField" class="file" id="fileField" size="28" style="width: 170px;">';
        HTML += '<input type="button" id="avatar_btn" class="btn" value="上传头像" size="28" />';
        HTML += '</form>';
        HTML += '<img src="/static/image/getAvatar.jpg" id="avatar">';
        HTML += '<span></span> ，你好';
        HTML += '<button id="logout">登出</button>';
        HTML += '</div>';
        HTML += '</div>';
        HTML += '<div id="middle">';
        HTML += '<img src="/static/image/search.jpg">';
        HTML += '<div class="left">'
        HTML += '<input type="text" id="inp_search">'
        HTML += '<button >十度一下</button>'
        HTML += '</div>'
        HTML += '<ul id="keylist" style="display: none">'
        HTML += '</ul>'
        HTML += '</div>'
        HTML += '<div id="bottom">'
        HTML += '<p>本站不存储任何音频文件，数据来自各网站接口，仅供个人学习、研究或者欣赏</p>'
        HTML += '</div>'
        return HTML
    }
};


index.search_right = {
    html: function () {
        var HTML = '<div id="top">'
        HTML += '<div class="not-login" style="display: inline-block;">'
        HTML += '<a href="/v1/user/register">注册</a>'
        HTML += '<a href="/v1/user/login">登陆</a>'
        HTML += '</div>'
        HTML += '<div class="login" style="display: none;">'
        HTML += '<form action="" method="post" enctype="multipart/form-data" id="avatar_form" style="display: none;">'
        HTML += '<input type="file" name="fileField" class="file" id="fileField" size="28" style="width: 170px;">'
        HTML += '<input type="button" id="avatar_btn" class="btn" value="上传头像" size="28"/>'
        HTML += '</form>'
        HTML += '<img src="/static/image/getAvatar.jpg" id="avatar">'
        HTML += '<span></span>,你好'
        HTML += ' <button id="logout">登出</button>'
        HTML += '</div>'
        HTML += '</div>'
        HTML += '<ul id="keylist">'
        HTML += '</ul>'
        return HTML
    }
};
index.search_option = {
    html: function () {
        var HTML = '<div class="right">'
        HTML += '<div id="top_search_bottom"></div>'
        HTML += ' <div id="option_search">'
        HTML += '<ul>'
        HTML += '<li class="select" id="music">音乐</li>'
        HTML += '<li id="picture">图片</li>'
        HTML += '<li id="movie">电影</li>'
        HTML += '</ul>'
        HTML += '</div>'
        return HTML
    }
};

index.music = {
    html: function (index, title1, title2) {
        var HTML = '';
        HTML += '<ul id="left_first" class="left">';
        HTML += '<div id="left_first_title" style="font-size: 30px; color: red;">' + title1 + '</div>';
        HTML += '<li class="music_title">';
        HTML += '<ul>';
        HTML += '<li>序号</li>';
        HTML += '<li>歌曲</li>';
        HTML += '<li>歌手</li>';
        HTML += '<li>时长</li>';
        HTML += '<li>评分</li>';
        HTML += '<li>评论</li>';
        HTML += '</ul>';
        HTML += '</li>';
        HTML += '</ul>';
        if (index >= 2) {
            HTML += '<ul id="left_first" class="right">';
            HTML += '<div id="left_first_title" style="font-size: 30px; color:#31c27c;">' + title2 + '</div>';
            HTML += '<li class="music_title">';
            HTML += '<ul>';
            HTML += '<li>序号</li>';
            HTML += '<li>歌曲</li>';
            HTML += '<li>歌手</li>';
            HTML += '<li>时长</li>';
            HTML += '<li>评分</li>';
            HTML += '<li>评论</li>';
            HTML += '</ul>';
            HTML += '</li>';
            HTML += '</ul>';
        }
        HTML += 'return HTML';
        return HTML
    }
};
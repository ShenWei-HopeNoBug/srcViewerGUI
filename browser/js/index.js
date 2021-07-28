//创建一个包裹了img的li标签
function createImgItem(path, index, setSrc = false) {
  //加载中动图
  const img = $('<img/>', {
    src: '../src/img/loading.gif',
    alt: `img_${index}`,
  })[0];
  //判断是否是超出大小范围的路径(第一个字符是否是#)
  if (path.startsWith('#')) {
    img.outsize = '../src/img/outSize.jpg'
    path = path.slice(1)
  }
  //错误加载
  img.onerror = function () {
    this.src = '../src/img/loadError.jpg';
  }
  img.title = path;
  img.preLoad = true;
  //是否是第一张图片
  if (setSrc) {
    img.first = true;
  }
  //一张一张顺序加载
  img.onload = function () {
    //第一次加载显示图片
    if (this.preLoad) {
      this.preLoad = false;
      if (this.first) {
        //是否超出大小
        if (!this.outsize) {
          this.src = this.title;
        } else {
          this.src = this.outsize;
        }
      }
      return;
    }
    //加载下一张图片
    const nextImg = $(this).parent().next().children('img')[0];
    if (nextImg) {
      if (nextImg.outsize && (nextImg.src !== nextImg.outsize)) {
        // 加载超出大小范围图片
        nextImg.src = nextImg.outsize;
        nextImg.outsize = undefined;   //清除临时变量
      } else if (nextImg.src !== nextImg.title) {
        //加载对应图片
        nextImg.src = nextImg.title;
      }
    }
    this.outsize = undefined;   //清除临时变量
  }
  return $('<li></li>').append(img)[0];
}

//创建一个包裹了(video和简介div)的li标签
function createVideoItem(path, index) {
  //--------视频
  const video = $('<video/>', {
    controls: true,
    preload: 'metadata'
  })[0];
  //判断是否是超出大小范围的路径(第一个字符是否是#)
  if (path.startsWith('#')) {
    video.src = '../src/video/outSize.mp4'
    path = path.slice(1)
  } else {
    video.src = path
  }
  //加载错误
  video.onerror = function () {
    this.src = "../src/video/loadError.mp4"
  }
  //------简介
  const info = path.split("/");
  const generalInfo = $('<div></div>')
    .addClass('info-general')
    .html(`<span>【${index}】</span><span>${info[info.length - 1]}</span>`)[0];
  //-------详细信息
  const detailInfo = $('<div></div>')
    .addClass('info-details')
    .html(`<span>${path}</span>
      <div class="tri">
        <div class="tri-out"></div>
        <div class="tri-in"></div>
        <div class="tri-out"></div>
        <div class="tri-in"></div>
      </div>`)[0];
  //------视频信息包裹外壳
  const videoInfo = $('<div></div>')
    .addClass('video-info')
    .append(generalInfo, detailInfo)[0];
  videoInfo.onmouseover = function () {
    this.lastChild.style.visibility = 'visible';
  };
  videoInfo.onmouseout = function () {
    this.lastChild.style.visibility = '';
  }
  //返回li标签
  return $('<li></li>').append(video, videoInfo)[0];
}

//在指定ul内替换生成li标签
function insertLiItems(pathList, ulID, createFunc, startIndex, setSrc = false) {
  const ul = $(`#${ulID}`);
  pathList.forEach((path, index) => {
    let li;
    if (index === 0) {
      //第一张图片设置src
      li = createFunc(path, startIndex + index, setSrc);
    } else {
      li = createFunc(path, startIndex + index);
    }
    ul.append(li);
  });
}

//为ul绑定图片浏览点击事件
function imgViewListen(ulID) {
  //事件委托绑定再自动点击
  $(`#${ulID}`).click((event) => {
    const img = event.target;
    //动态添加点击事件
    if (!img.addView) {
      new Viewer(img);
      img.addView = true;
      img.click();
    }
  });
}

//为ul绑定video相关事件
function videoListen(ulID) {
  const videos = $(`#${ulID}`).find('video');
  const len = videos.length;
  let count = 0;
  for (let i = 0; i < len; i++) {
    videos[i].addEventListener("play", () => {
      count++;
      if (count > 1) {
        videos[i].pause();
      }
    });
    videos[i].addEventListener("pause", () => {
      count--;
    });
  }
}

//显示页数
function pageShow(num, start, end) {
  $('#page').text(`第 ${num} 页`);
  $('#img-num').text(`( ${start} - ${end} )`);
}

//限制页数
function pageLimit(page) {
  if (page > pageMax) {
    page = pageMax
  }
  if (page < 1) {
    page = 1
  }
  return page
}

//刷新页面显示
function refreshPage(start, end, first = false) {
  if (pathLength === 0) {
    pageShow(page, 0, 0);
  } else {
    pageShow(page, start + 1, end);
    switch (listType) {
      case "image":
        if (first) {
          //第一次加载页面
          insertLiItems(pathList.slice(start, end), "images",
            createImgItem, start + 1, true);
          imgViewListen("images");
        } else {
          //切换页面
          refreshList(start, end, 'images');
        }
        break;

      case "video":
        if (first) {
          //第一次加载页面
          insertLiItems(pathList.slice(start, end), "videos",
            createVideoItem, start + 1, true);
        } else {
          //切换页面
          refreshList(start, end, 'videos');
        }
        videoListen("videos");
        break;
    }
  }
}

//刷新增减资源li外壳的个数
function refreshList(start, end, ulID) {
  let replaceList = pathList.slice(start, end)
  const list = $(`#${ulID} li`)
  //对比输入路径长度和img标签个数
  if (replaceList.length > list.length) {
    const insertStart = start + list.length; //开始插入的索引
    //补齐缺失的li
    switch (listType) {
      case "image":
        insertLiItems(
          pathList.slice(insertStart, end),
          "images",
          createImgItem,
          insertStart + 1,
        );
        break;

      case "video":
        insertLiItems(
          pathList.slice(insertStart, end),
          "videos",
          createVideoItem,
          insertStart + 1,
        );
    }
    //修剪需要替换的src
    replaceList = replaceList.slice(0, list.length)
  } else if (replaceList.length < list.length) {
    //删除多出的li
    list.slice(replaceList.length).remove()
  }
  //修改src
  switch (listType) {
    case "image":
      replaceImageSrc(replaceList, ulID);
      break;

    case "video":
      replaceVideoSrc(replaceList, ulID);
  }
}

//换页修改图片资源路径
function replaceImageSrc(replaceList, ulID) {
  const imgList = $(`#${ulID} img`)
  //替换路径
  for (let index = 0; index < replaceList.length; index++) {
    let path = replaceList[index]
    //判断是否是超出大小范围的路径(第一个字符是否是#)
    if (path.startsWith('#')) {
      imgList[index].outsize = '../src/img/outSize.jpg'
      path = path.slice(1)
    }
    //修改属性
    imgList.eq(index).attr({
      'title': path,
      'alt': `img_${start + index + 1}`,
      'src': "../src/img/loading.gif"
    })
    imgList[index].preLoad = true;
  }
}

//换页修改视频资源路径
function replaceVideoSrc(replaceList, ulID) {
  const ul = $(`#${ulID}`);
  const videoList = ul.find('video');
  const generalInfo = ul.find('.info-general');
  const detailInfo = ul.find('.info-details');

  //替换路径
  for (let index = 0; index < replaceList.length; index++) {
    let path = replaceList[index]
    //判断是否是超出大小范围的路径(第一个字符是否是#)
    if (path.startsWith('#')) {
      videoList[index].src = '../src/video/outSize.mp4'
      path = path.slice(1)
    } else {
      videoList[index].src = path;
    }
    //修改简介
    const info = path.split("/");
    generalInfo.eq(index).find('span').eq(0).text(`【${start + index + 1}】`);
    generalInfo.eq(index).find('span').eq(1).text(info[info.length - 1]);
    detailInfo.eq(index).find('span').text(path)
  }
}

//换页前后按钮禁用管理，callback为换页回调
function buttonDisable(callback) {
  if (end === pathLength) {
    end = pathLength;
    $('#btn-next').attr('disabled', false);
  }
  if (start === 0) {
    $('#btn-pre').attr('disabled', false);
  }
  callback();   //换页回调
  start = (page - 1) * num;
  end = page * num;
  if (end >= pathLength) {
    end = pathLength;
    $('#btn-next').attr('disabled', true);
  }
  if (start === 0) {
    $('#btn-pre').attr('disabled', true);
  }
}

//绑定换页按钮事件
function pageChange() {
  //----------前进
  $('#btn-next').click(() => {
    buttonDisable(() => {
      page++
    });
    refreshPage(start, end);
  })
  //-----------后退
  $('#btn-pre').click(() => {
    buttonDisable(() => {
      page--
    });
    refreshPage(start, end);
  })
  //全局按键
  $(document).keyup(event => {
    switch (event.keyCode) {
      case 68: {
        //D键下一页
        const next_btn = $('#btn-next')[0];
        if (!next_btn.disabled) {
          next_btn.click();
        }
        break;
      }
      case 65: {
        //A键上一页
        const next_btn = $('#btn-pre')[0];
        if (!next_btn.disabled) {
          next_btn.click();
        }
        break;
      }
    }
  })
  //输入框按键
  $('#page-input').keyup(event => {
    if (event.keyCode === 13) {
      $('#btn-jump').click();
    }
  })
}

//初始化显示
function init() {
  //按情况禁用换页按钮
  if (end >= pathLength) {
    end = pathLength;
    $("#btn-next").attr('disabled', true);
  }
  if (start === 0) {
    $("#btn-pre").attr('disabled', true);
  }
  refreshPage(start, end, true);     //初始化页面

  const btn_jump = $("#btn-jump");
  if (pageMax <= 1) {
    pageMax = 1;
    //页面小于一页禁用按钮和输入
    btn_jump.attr('disabled', true);
    $('#page-input').attr('disabled', true);
  } else {
    //页面大于一页绑定按钮事件
    btn_jump.click(() => {
      const pageInput = $("#page-input");
      let pageTo = pageInput.val();
      const pageToNum = pageLimit(parseInt(pageTo));
      //输入数字字符处理
      if ((pageTo !== '') && (pageToNum !== page)) {
        buttonDisable(() => {
          page = pageToNum;
        });
        refreshPage(start, end);
      }
      pageInput.val('');
    })
    //显示页数信息
    $('#page-sum').text(`共 ${pageMax} 页`);
    pageChange();
    //限制输入上限
    $('#page-input').attr('max', pageMax.toString())
  }
}

//--------------全局变量
const pathLength = pathList.length;
let pageMax,  //单页面最大显示数量
  start,  //pathList显示起始index
  end;  //pathList显示末尾index
//初始化全局变量
let num;
switch (listType) {
  case "image":
    num = 5 * maxRow;
    break;
  case "video":
    num = 2 * maxRow;
    break;
}
pageMax = pathLength % num === 0 ? pathLength / num : parseInt(pathLength / num) + 1;
page = pageLimit(page);
start = (page - 1) * num;
end = page * num;

//------------初始化
$(document).ready(() => {
  init();
});







//����һ��������img��li��ǩ
function createImgItem(path, index, setSrc = false) {
  //�����ж�ͼ
  const img = $('<img/>', {
    src: '../src/img/loading.gif',
    alt: `img_${index}`,
  })[0];
  //�ж��Ƿ��ǳ�����С��Χ��·��(��һ���ַ��Ƿ���#)
  if (path.startsWith('#')) {
    img.outsize = '../src/img/outSize.jpg'
    path = path.slice(1)
  }
  //�������
  img.onerror = function () {
    this.src = '../src/img/loadError.jpg';
  }
  img.title = path;
  img.preLoad = true;
  //�Ƿ��ǵ�һ��ͼƬ
  if (setSrc) {
    img.first = true;
  }
  //һ��һ��˳�����
  img.onload = function () {
    //��һ�μ�����ʾͼƬ
    if (this.preLoad) {
      this.preLoad = false;
      if (this.first) {
        //�Ƿ񳬳���С
        if (!this.outsize) {
          this.src = this.title;
        } else {
          this.src = this.outsize;
        }
      }
      return;
    }
    //������һ��ͼƬ
    const nextImg = $(this).parent().next().children('img')[0];
    if (nextImg) {
      if (nextImg.outsize && (nextImg.src !== nextImg.outsize)) {
        // ���س�����С��ΧͼƬ
        nextImg.src = nextImg.outsize;
        nextImg.outsize = undefined;   //�����ʱ����
      } else if (nextImg.src !== nextImg.title) {
        //���ض�ӦͼƬ
        nextImg.src = nextImg.title;
      }
    }
    this.outsize = undefined;   //�����ʱ����
  }
  return $('<li></li>').append(img)[0];
}

//����һ��������(video�ͼ��div)��li��ǩ
function createVideoItem(path, index) {
  //--------��Ƶ
  const video = $('<video/>', {
    controls: true,
    preload: 'metadata'
  })[0];
  //�ж��Ƿ��ǳ�����С��Χ��·��(��һ���ַ��Ƿ���#)
  if (path.startsWith('#')) {
    video.src = '../src/video/outSize.mp4'
    path = path.slice(1)
  } else {
    video.src = path
  }
  //���ش���
  video.onerror = function () {
    this.src = "../src/video/loadError.mp4"
  }
  //------���
  const info = path.split("/");
  const generalInfo = $('<div></div>')
    .addClass('info-general')
    .html(`<span>��${index}��</span><span>${info[info.length - 1]}</span>`)[0];
  //-------��ϸ��Ϣ
  const detailInfo = $('<div></div>')
    .addClass('info-details')
    .html(`<span>${path}</span>
      <div class="tri">
        <div class="tri-out"></div>
        <div class="tri-in"></div>
        <div class="tri-out"></div>
        <div class="tri-in"></div>
      </div>`)[0];
  //------��Ƶ��Ϣ�������
  const videoInfo = $('<div></div>')
    .addClass('video-info')
    .append(generalInfo, detailInfo)[0];
  videoInfo.onmouseover = function () {
    this.lastChild.style.visibility = 'visible';
  };
  videoInfo.onmouseout = function () {
    this.lastChild.style.visibility = '';
  }
  //����li��ǩ
  return $('<li></li>').append(video, videoInfo)[0];
}

//��ָ��ul���滻����li��ǩ
function insertLiItems(pathList, ulID, createFunc, startIndex, setSrc = false) {
  const ul = $(`#${ulID}`);
  pathList.forEach((path, index) => {
    let li;
    if (index === 0) {
      //��һ��ͼƬ����src
      li = createFunc(path, startIndex + index, setSrc);
    } else {
      li = createFunc(path, startIndex + index);
    }
    ul.append(li);
  });
}

//Ϊul��ͼƬ�������¼�
function imgViewListen(ulID) {
  //�¼�ί�а����Զ����
  $(`#${ulID}`).click((event) => {
    const img = event.target;
    //��̬��ӵ���¼�
    if (!img.addView) {
      new Viewer(img);
      img.addView = true;
      img.click();
    }
  });
}

//Ϊul��video����¼�
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

//��ʾҳ��
function pageShow(num, start, end) {
  $('#page').text(`�� ${num} ҳ`);
  $('#img-num').text(`( ${start} - ${end} )`);
}

//����ҳ��
function pageLimit(page) {
  if (page > pageMax) {
    page = pageMax
  }
  if (page < 1) {
    page = 1
  }
  return page
}

//ˢ��ҳ����ʾ
function refreshPage(start, end, first = false) {
  if (pathLength === 0) {
    pageShow(page, 0, 0);
  } else {
    pageShow(page, start + 1, end);
    switch (listType) {
      case "image":
        if (first) {
          //��һ�μ���ҳ��
          insertLiItems(pathList.slice(start, end), "images",
            createImgItem, start + 1, true);
          imgViewListen("images");
        } else {
          //�л�ҳ��
          refreshList(start, end, 'images');
        }
        break;

      case "video":
        if (first) {
          //��һ�μ���ҳ��
          insertLiItems(pathList.slice(start, end), "videos",
            createVideoItem, start + 1, true);
        } else {
          //�л�ҳ��
          refreshList(start, end, 'videos');
        }
        videoListen("videos");
        break;
    }
  }
}

//ˢ��������Դli��ǵĸ���
function refreshList(start, end, ulID) {
  let replaceList = pathList.slice(start, end)
  const list = $(`#${ulID} li`)
  //�Ա�����·�����Ⱥ�img��ǩ����
  if (replaceList.length > list.length) {
    const insertStart = start + list.length; //��ʼ���������
    //����ȱʧ��li
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
    //�޼���Ҫ�滻��src
    replaceList = replaceList.slice(0, list.length)
  } else if (replaceList.length < list.length) {
    //ɾ�������li
    list.slice(replaceList.length).remove()
  }
  //�޸�src
  switch (listType) {
    case "image":
      replaceImageSrc(replaceList, ulID);
      break;

    case "video":
      replaceVideoSrc(replaceList, ulID);
  }
}

//��ҳ�޸�ͼƬ��Դ·��
function replaceImageSrc(replaceList, ulID) {
  const imgList = $(`#${ulID} img`)
  //�滻·��
  for (let index = 0; index < replaceList.length; index++) {
    let path = replaceList[index]
    //�ж��Ƿ��ǳ�����С��Χ��·��(��һ���ַ��Ƿ���#)
    if (path.startsWith('#')) {
      imgList[index].outsize = '../src/img/outSize.jpg'
      path = path.slice(1)
    }
    //�޸�����
    imgList.eq(index).attr({
      'title': path,
      'alt': `img_${start + index + 1}`,
      'src': "../src/img/loading.gif"
    })
    imgList[index].preLoad = true;
  }
}

//��ҳ�޸���Ƶ��Դ·��
function replaceVideoSrc(replaceList, ulID) {
  const ul = $(`#${ulID}`);
  const videoList = ul.find('video');
  const generalInfo = ul.find('.info-general');
  const detailInfo = ul.find('.info-details');

  //�滻·��
  for (let index = 0; index < replaceList.length; index++) {
    let path = replaceList[index]
    //�ж��Ƿ��ǳ�����С��Χ��·��(��һ���ַ��Ƿ���#)
    if (path.startsWith('#')) {
      videoList[index].src = '../src/video/outSize.mp4'
      path = path.slice(1)
    } else {
      videoList[index].src = path;
    }
    //�޸ļ��
    const info = path.split("/");
    generalInfo.eq(index).find('span').eq(0).text(`��${start + index + 1}��`);
    generalInfo.eq(index).find('span').eq(1).text(info[info.length - 1]);
    detailInfo.eq(index).find('span').text(path)
  }
}

//��ҳǰ��ť���ù���callbackΪ��ҳ�ص�
function buttonDisable(callback) {
  if (end === pathLength) {
    end = pathLength;
    $('#btn-next').attr('disabled', false);
  }
  if (start === 0) {
    $('#btn-pre').attr('disabled', false);
  }
  callback();   //��ҳ�ص�
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

//�󶨻�ҳ��ť�¼�
function pageChange() {
  //----------ǰ��
  $('#btn-next').click(() => {
    buttonDisable(() => {
      page++
    });
    refreshPage(start, end);
  })
  //-----------����
  $('#btn-pre').click(() => {
    buttonDisable(() => {
      page--
    });
    refreshPage(start, end);
  })
  //ȫ�ְ���
  $(document).keyup(event => {
    switch (event.keyCode) {
      case 68: {
        //D����һҳ
        const next_btn = $('#btn-next')[0];
        if (!next_btn.disabled) {
          next_btn.click();
        }
        break;
      }
      case 65: {
        //A����һҳ
        const next_btn = $('#btn-pre')[0];
        if (!next_btn.disabled) {
          next_btn.click();
        }
        break;
      }
    }
  })
  //����򰴼�
  $('#page-input').keyup(event => {
    if (event.keyCode === 13) {
      $('#btn-jump').click();
    }
  })
}

//��ʼ����ʾ
function init() {
  //��������û�ҳ��ť
  if (end >= pathLength) {
    end = pathLength;
    $("#btn-next").attr('disabled', true);
  }
  if (start === 0) {
    $("#btn-pre").attr('disabled', true);
  }
  refreshPage(start, end, true);     //��ʼ��ҳ��

  const btn_jump = $("#btn-jump");
  if (pageMax <= 1) {
    pageMax = 1;
    //ҳ��С��һҳ���ð�ť������
    btn_jump.attr('disabled', true);
    $('#page-input').attr('disabled', true);
  } else {
    //ҳ�����һҳ�󶨰�ť�¼�
    btn_jump.click(() => {
      const pageInput = $("#page-input");
      let pageTo = pageInput.val();
      const pageToNum = pageLimit(parseInt(pageTo));
      //���������ַ�����
      if ((pageTo !== '') && (pageToNum !== page)) {
        buttonDisable(() => {
          page = pageToNum;
        });
        refreshPage(start, end);
      }
      pageInput.val('');
    })
    //��ʾҳ����Ϣ
    $('#page-sum').text(`�� ${pageMax} ҳ`);
    pageChange();
    //������������
    $('#page-input').attr('max', pageMax.toString())
  }
}

//--------------ȫ�ֱ���
const pathLength = pathList.length;
let pageMax,  //��ҳ�������ʾ����
  start,  //pathList��ʾ��ʼindex
  end;  //pathList��ʾĩβindex
//��ʼ��ȫ�ֱ���
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

//------------��ʼ��
$(document).ready(() => {
  init();
});







// !function(){}() 或 (function(){})()
!function () {

    function resolvePath(path) {
        const segments = path.split('/');
        let resolved = [];
        for (let i=0, len=segments.length; i<len; i++){
            if (segments[i] === '..') {
                resolved.pop();
            } else if (segments[i] !== '.') {
                resolved.push(segments[i]);
            }
        }
        return resolved.join('/');
    }

    // 对class name包括path-append的含href的元素进行路径增添
    function docsifyAppendPath(hook, vm) {

        hook.doneEach(function() {
            const DOM = document;
            if (DOM) {
                let els = DOM.getElementsByClassName('path-append');
                let len = els.length;
                if (len > 0){
                    // get the local directory, note directory always ends with '/'
                    let dir = DOM.URL.replace(/^[^#]*\/#\//,'').replace(/\/(?!.*\/).*/, '');

                    for (let i=len; i--; ){
                        let hrefNode = els[i].attributes['href'];
                        let oldHref = hrefNode? hrefNode.nodeValue : "";

                        if (oldHref && !oldHref.startsWith(DOM.location.origin)){
                            if (oldHref.startsWith('#/')){
                                hrefNode.nodeValue  = '#/' + resolvePath(dir + oldHref.substring(1)); // pop #
                            } else {
                                hrefNode.nodeValue  = resolvePath(dir + '/' + oldHref.replace(/^\.\//, '').replace(/^\//, ''));
                            }
                        }
                    }
                }
            }
        });
    }

    // 对class name为download的a含href的元素添加download属性
    function docsifyDownload(hook, vm) {
        hook.doneEach(function() {
            const DOM = document;
            if (DOM) {
                let els = DOM.querySelectorAll('a.download');
                for (let i=els.length; i--; ) {
                    let el = els[i];
                    let hrefNode = el.attributes['href'];
                    let href = hrefNode? hrefNode.nodeValue : "";
                    if (href && !href.endsWith('/')) {
                        let downloadNode = el.attributes['download'];
                        if (typeof downloadNode === 'undefined') {
                            downloadNode = DOM.createAttribute('download');
                            el.attributes.setNamedItem(downloadNode);
                        }
                        if (!downloadNode.nodeValue) {
                            downloadNode.nodeValue = href.split('/').pop(-1);
                        }
                    }
                }
            }
        });
    }

    // use scrollIntoView function to locate the anchor point In the same page
    function scrollIntoViewById(id, f) {
        f = typeof f !== 'undefined' ? f : true;
        let el = document.getElementById(id);
        el && el.scrollIntoView(f);
    }

    // 防抖处理
    !function () {
        function debounce(fn, delay) {
            let timer = null;
            return (...args) => {
                clearTimeout(timer);
                timer = setTimeout(()=>{fn.apply(this, args);},delay);
            };
        }

        scrollIntoViewById = debounce(scrollIntoViewById, 50);
    }();

    function scrollIntoReferAnchor(f) {
        scrollIntoViewById('refer-anchor', f);
        return false;
    }

    // 使用scrollIntoView对参考资料id为refer-anchor的参考资料定位点进行定位
    function docsifyRefer(hook, vm) {
        hook.doneEach(function(){
            const DOM = document;
            if (DOM) {
                let els = DOM.querySelectorAll('a.refer');
                for (let i=els.length; i--; ) {
                    let el = els[i];
                    el.onclick = scrollIntoReferAnchor; 
                    el.href || (el.href = "javascript:void(0);");
                }
            }
        })
    }

    // docsify plugins
    if (window) {
        window.$docsify = window.$docsify || {};

        window.$docsify.plugins = [].concat(
            (window.$docsify.plugins || []),
            docsifyAppendPath,
            docsifyDownload,
            docsifyRefer
        );
    }

}();
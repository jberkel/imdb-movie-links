// based on http://code.google.com/p/svgpan/
// (andrea.leofreddi)
(function($) {
  function init(svgDoc) {
    var state = 'none', stateTarget, stateOrigin, stateTf;

    var root = svgDoc.documentElement,
           g = svgDoc.getElementById('graph1');

    root.removeAttribute('viewBox');
    //root.setAttribute('viewBox', '0 0 500 500');
    setupHandlers(svgDoc);

    /**
     * Register handlers
     */
    function setupHandlers(doc){
      doc.onmousedown = handleMouseDown;
      doc.onmousemove = handleMouseMove;
      doc.onmouseup   = handleMouseUp;

      if(navigator.userAgent.toLowerCase().indexOf('webkit') >= 0) {
        window.addEventListener('mousewheel', handleMouseWheel, false); // Chrome/Safari
      } else {
        window.addEventListener('DOMMouseScroll', handleMouseWheel, false); // Others
      }
    }

    /**
     * Instance an SVGPoint object with given event coordinates.
     */
    function getEventPoint(evt) {
      var p = root.createSVGPoint();
      p.x = evt.clientX;
      p.y = evt.clientY;
      return p;
    }

    /**
     * Sets the current transform matrix of an element.
     */
    function setCTM(element, matrix) {
      var s = "matrix(" + matrix.a + "," + matrix.b + "," + matrix.c + "," + matrix.d + "," +
                          matrix.e + "," + matrix.f + ")";
      //console.log(s);
      if (matrix.a > 0.04) {
        element.setAttribute("transform", s);
      }
    }

    /**
     * Dumps a matrix to a string (useful for debug).
     */
    function dumpMatrix(matrix) {
      var s = "[ " + matrix.a + ", " + matrix.c + ", " + matrix.e + "\n  " + matrix.b + ", " +
                     matrix.d + ", " + matrix.f + "\n  0, 0, 1 ]";
      return s;
    }

    /**
     * Sets attributes of an element.
     */
    function setAttributes(element, attributes){
      for (i in attributes)
        element.setAttributeNS(null, i, attributes[i]);
    }

    /**
     * Handle mouse move event.
     */
    function handleMouseWheel(evt) {
      if(evt.preventDefault)
        evt.preventDefault();

      evt.returnValue = false;
      var delta;

      if(evt.wheelDelta) {
        //console.log(evt.wheelDelta);
        if (navigator.vendor &&
            navigator.vendor.indexOf("Apple") != -1) {
          delta = evt.wheelDelta / 3600; // Chrome/Safari
        } else {
          delta = evt.wheelDelta / 1200;
        }
      } else {
        delta = evt.detail / -90; // Mozilla
      }

      var z = 1 + delta; // Zoom factor: 0.9/1.1
      var p = getEventPoint(evt);

      p = p.matrixTransform(g.getCTM().inverse());

      // Compute new scale matrix in current mouse position
      var k = root.createSVGMatrix().translate(p.x, p.y).scale(z).translate(-p.x, -p.y);
      setCTM(g, g.getCTM().multiply(k));

      if (stateTf) {
        stateTf = stateTf.multiply(k.inverse());
      }
    }

    /**
     * Handle mouse move event.
     */
    function handleMouseMove(evt) {
      if(evt.preventDefault)
        evt.preventDefault();

      evt.returnValue = false;

      if(state == 'pan') {
        evt.target.style.cursor = 'move';

        $('g.node ellipse', svgDoc).each(function() {
          $(this).attr('fill', 'yellow');
        });

        // Pan mode
        var p = getEventPoint(evt).matrixTransform(stateTf);
        setCTM(g, stateTf.inverse().translate(p.x - stateOrigin.x, p.y - stateOrigin.y));
      } else if(state == 'move') {
        // Move mode
        var p = getEventPoint(evt).matrixTransform(g.getCTM().inverse());

        setCTM(stateTarget,
               svgDoc
                .createSVGMatrix()
                .translate(p.x - stateOrigin.x, p.y - stateOrigin.y)
                .multiply(g.getCTM().inverse())
                .multiply(stateTarget.getCTM()));

        stateOrigin = p;
      }
    }

    /**
     * Handle click event.
     */
    function handleMouseDown(evt) {
      if(evt.preventDefault)
        evt.preventDefault();

      evt.returnValue = false;

      stateTf = g.getCTM().inverse();
      stateOrigin = getEventPoint(evt).matrixTransform(stateTf);
      state = 'pan';

      /*
      if(evt.target.tagName == "svg") {
        // Pan mode
        state = 'pan';
     } else {
        // Move mode
        state = 'move';
        stateTarget = evt.target;
      }
      */
    }

    /**
     * Handle mouse button release event.
     */
    function handleMouseUp(evt) {
      if(evt.preventDefault)
        evt.preventDefault();

      evt.returnValue = false;

      if(state == 'pan' || state == 'move') {
        // Quit pan mode
        state = '';

        evt.target.style.cursor = 'auto';

        $('g.node ellipse', svgDoc).each(function() {
          $(this).attr('fill', 'none');
        });
      }
    }
 }

 SVGPan = function(svgDoc) {
    init(svgDoc);
 }
})(jQuery);

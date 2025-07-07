import { GridStack } from 'gridstack';
import 'gridstack/dist/gridstack.min.css';

document.addEventListener('DOMContentLoaded', () => {
  const grid = GridStack.init({
    cellHeight: 250,
    draggable: {
      handle: '.grid-stack-item-content'
    },
    resizable: {
      handles: 'e, se, s, sw, w'
    },
    float: true
  });
});


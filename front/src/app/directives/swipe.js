import { reactive } from 'vue';

const state = reactive({
  isDown: false,
  startX: 0,
  el: undefined
});

function listenMouseDown(e) {
  if (state.el) {
    state.isDown = true;
    state.el.style.transition = undefined
    state.startX = e.clientX;
    state.el.style.cursor = 'grabbing';
  }
}

function listenMouseLeave() {
  if (state.el) {
    state.isDown = false;
    state.el.style.cursor = 'grab';
  }
}

function listenMouseUp() {
  if (state.el) {
    state.isDown = false;
    state.el.style.transition = 'left 0.3s ease'
    state.el.style.cursor = 'grab';
    if(Number(state.el.style.left.slice(0,-2))< -(state.el.clientWidth+24)){
      state.el.dispatchEvent(new CustomEvent('swiped', {
        detail: 'left'
      }))
    }else if(Number(state.el.style.left.slice(0,-2)) > state.el.clientWidth+24){
      state.el.dispatchEvent(new CustomEvent('swiped', {
        detail: 'right'
      }))
    }else{
      state.el.style.left = '0'
    }
  }
}

function listenMouseMove(e) {
  if (!state.isDown || !state.el) return;
  
  const walkX = (e.clientX - state.startX) * 1;
  state.el.style.opacity='1'
  state.el.style.left = walkX + 'px';
}

export default {
  mounted(el) {
    state.el = el;
    state.el.style.position = 'absolute'
    state.el.addEventListener('mousedown', listenMouseDown);

    state.el.addEventListener('mouseleave', listenMouseLeave);
    document.addEventListener('mouseup', listenMouseUp);

    document.addEventListener('mousemove', listenMouseMove);
    return;
  },

  beforeUnmount() {
    if (!state.el) return;

    state.el.removeEventListener('mousedown', listenMouseDown);

    state.el.removeEventListener('mouseleave', listenMouseLeave);
    document.removeEventListener('mouseup', listenMouseLeave);

    document.removeEventListener('mousemove', listenMouseMove);
  }
};

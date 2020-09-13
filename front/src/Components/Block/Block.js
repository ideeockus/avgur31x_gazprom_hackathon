import React from 'react';
import './Block.css'

function Block(props) {
  return (
    <div
      className="Block"
      style={{
        backgroundColor: props.color == null ? '#fff' : props.color,
      }, props.style}
    >
      {props.children}
    </div>
  );
}

export {
  Block
}

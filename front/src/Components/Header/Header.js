import React from 'react';
import './Header.css'
import {Block} from '../index'
import {
  LogoGpbBlueIcon,
} from '@holism/icons';

function Header(props) {
  return (
    <Block color="#fff" style={{
      borderColor: '#e6eaf0',
      borderBottomWidth: 2,
      borderBottomStyle: 'solid',
    }}>
      <div className="inner">
        <div className="Header">
          <div className="logo">
            <LogoGpbBlueIcon/>
          </div>
          <div className="projName">
            ПОТОКОВАЯ АНАЛИТИКА (pre-alpha)
          </div>
        </div>
      </div>
    </Block>
  );
}

export {
  Header
}

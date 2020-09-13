import React from 'react';
import { Container, Flex, GridCol, Grid } from '@holism/core';
import {Header, Block} from './Components'
import './App.css';

const bg = require('./assets/images/man.png');

function App() {
  return (
    <div>
      <Header/>
      <Block>
        <div className="bg">
          <img src={bg}/>
        </div>
        <div className="inner">
          <div className="text_img">
            <h1>Сервис для анализа потока данных и генерации событий.</h1>
            Наше решение — это сервис, который основываясь на передвижении
            людей, выявляет дополнительные данные, о каждом из них, такие как: наличие
            детей, место работы, маршруты и расположения дома.
            <br/><br/>Сервис сигнализирует,
            когда считает, что определенный пользователь является потенциальным
            клиентом банка, автозаправки или строек партнеров, для последующей
            агитации.
          </div>
        </div>
      </Block>
      <Block>
        <div className="inner">
          <div className="text">
            <h1>Список событий:</h1>
            <div className="console">
              TODO: output
              {//TODO: объеденить
              }
            </div>
          </div>
        </div>
      </Block>
    {/*
      <Block>
        <div className="inner">
          <div className="text">
            <h1>Карта:</h1>
          </div>
        </div>
      </Block>
      */}
      <Block style={{backgroundColor: "#3f5ddb"}}>
        <div className="inner">
          <div className="footer">
            <center>
              <h2>Avgur31x 2020</h2>
            </center>
          </div>
        </div>
      </Block>
    </div>
  );
}

export default App;

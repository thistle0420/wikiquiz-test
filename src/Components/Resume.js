import React, { Component } from "react";
import Slide from "react-reveal";
import Data from '../python/data.json';

const wikiList = Data.data.wiki;

class Resume extends Component {
  getRandomColor() {
    let letters = "0123456789ABCDEF";
    let color = "#";
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }

  render() {
    if (!this.props.data) return null;

    const getWikiTime = (num) => {
      return wikiList[num].datetime
    }

    const getWikiUrl = (num) => {
      return wikiList[num].url
    }

    const getWikiText = (num) => {
      return wikiList[num].text
    }

    const question = (num) => {
      return (
        <Slide left duration={1300}>
          <div className="row work">
            <div className="three columns header-col">
            <h1>
                <span>Question {num}</span>
              </h1>
              <h1>
                <span>({getWikiTime(num-1)})</span>
              </h1>
            </div>

            <div className="nine columns main-col">
              <div className="row item">
                <div className="twelve columns">
                  <p>{getWikiText(num-1)}</p>
                  <a href={getWikiUrl(num-1)}>
                    → 答えはこちら
                  </a>
                </div>
              </div>
            </div>
          </div>
        </Slide>
      )
    }

    const allQuestion = () => {
      const items = [];
      for (let i=1; i<=wikiList.length; i++) {
        items.push(question(i))
      }
      return <div>{ items }</div>;
    }

    return (
      <section id="resume">
        {allQuestion()}
      </section>
    );
  }
}

export default Resume;

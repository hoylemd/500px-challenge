import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

class PhotoCard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }
  render() {
    return (
      <div class="photo_card">
        <div>{ this.props.name }</div>
          <img class="thumbnail" src={ this.props.src }/>
        <div class='author'>By: { this.props.author }</div>
      </div>
    )
  }
}

class PhotoPage extends React.Component {
  createCard(photo) {
    return (
      <PhotoCard
        id={photo.id}
        name={photo.name}
        src={photo.images[0].https_url}
        author={photo.user.username}
      />
    )
  }

  createCards() {
    let cards = []
    for (let i=0; i < this.props.photos.length; i +=1) {
      cards.push(this.createCard(this.props.photos[i]));
    }

    return cards;
  };

  render() {
    return (
      <div class="photo_page">
        <h3>The current most popular {this.props.photos.length} photos on 500px</h3>

        {this.createCards()}

      </div>
    )
  }
}

class Showcase extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      photos: null,
      rpp: 8,
      page: 1
    }

    this.getPhotos();
  }

  getPhotos(rpp=8, page=1) {
    let url = '/bff/?rpp=' + rpp + '&page=' + 1;


    window.fetch('/bff/').then((response) => {
      return response.json();
    }).then((blob) => {
      this.setState({
        photos: blob.photos,
        page: blob.currentPage,
        rpp: blob
      });
    });

    this.setState({
      photos: null,
      rpp: rpp,
      page: page
    });
  }

  render() {
    if (this.state.photos === null) {
      return 'loading...';
    } else {
      return (
        <PhotoPage
          photos={this.state.photos}
          page={this.state.page}
          rpp={this.state.rpp}
        />
      )
    }
  }
}
ReactDOM.render(
  <Showcase />,
  document.getElementById('root')
);

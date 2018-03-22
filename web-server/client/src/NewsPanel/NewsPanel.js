import './NewsPanel.css'
import Auth from '../Auth/Auth'
import React from 'react';
import NewsCard from '../NewsCard/NewsCard';
import _ from 'lodash';
class NewsPanel extends React.Component{
    constructor(){
        super();
        this.state = {news: null, 
                      pageNum: 1,
                      loadAll: false
                    };
    }
    
    componentDidMount(){
        this.loadMoreNews();
        this.loadMoreNews = _.debounce(this.loadMoreNews, 1000); // call loadMoreNews per second when scrolling; check after stop
        // this.handleScroll = _.throttle(this.handleScroll, 400); // checking constantly how far we are from the bottom.it will help us get more news before the bottom. 
        window.addEventListener('scroll', () => this.handleScroll());
    }

    handleScroll(){
        // the height that cannot show on the screen
        let scrollY = window.scrollY || window.pageYOffset ||
            document.documentElement.scrollTop;
        if ((window.innerHeight + scrollY) >= (document.body.offsetHeight - 50 )){
            this.loadMoreNews();
        }
    }

    loadMoreNews(){
        //connect to the sever to get the list of news
        const news_url = 'http://' + window.location.hostname 
                        + ':3000/news/userId/' + Auth.getEmail() + '/pageNum/' + this.state.pageNum;
        const request = new Request(encodeURI(news_url), {
                method: 'GET',
                headers: {
                    'authentication' : 'bearer ' + Auth.getToken()
                }
            }
        );

        fetch(request)
            .then(res => res.json())
            .then(news_list => {
                if(!news_list || news_list.length == 0){
                    this.setState({loadAll: true});
                } else {
                    this.setState({
                        news: this.state.news? this.state.news.concat(news_list): news_list,
                        pageNum: this.state.pageNum + 1
                    });
                }
            });
    }

    renderNews(){
        const news_card_list = this.state.news.map(news_card => {
            return (
                <a className='list-group-item' key={news_card.digest} href={news_card.url}>
                    <NewsCard news={news_card} />
                </a>
            );
        });
        return (
            <div className='container-fluid'>
                <div className='list-group'>
                    {news_card_list}
                </div>
            </div>
        );
    }

    render(){
        if(this.state.news){
            return (
                <div>
                    {this.renderNews()}
                </div>
            );     
        }else{
            return(
                <div id='msg-app-loading'>
                    Loading...
                </div>
            );
        }      
    };
} 
export default NewsPanel;
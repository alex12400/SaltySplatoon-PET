import React, { useState } from 'react';
import './App.css';
import {Collapse, Container, Col, Row, Button} from 'reactstrap'

class Reviews extends React.Component {
	constructor(props){
		super(props)
		this.state = {
			reviews: this.props.reviews,
			c: true
		}
		this.handleCollapse = this.handleCollapse.bind(this);
	}

	handleCollapse(index){
		let reviewsCopy = [...this.state.reviews];
		console.log(reviewsCopy);
		reviewsCopy[index].collapsed = !reviewsCopy[index].collapsed;
		this.setState({
			reviews: reviewsCopy
		})
	}

	Hidden = (reviewerName) => {
		var hiddentextarea = document.getElementById('textarea')
		if(hiddentextarea.style.display === 'none'){
			hiddentextarea.style.display = ''
		} else{
			hiddentextarea.style.display = 'none'
		}
	}

	render() {
        //console.log(this.props.todos)
        return this.state.reviews.map((review, index) => (
            <Container fluid='sm'>
                <p style={reviewstyle}>
                    <p onClick = {() => this.handleCollapse(index)}>
                        <Container>
                            <Row>
                            	<Col>
                                    <h4 style={h4inlinestyle}>{ review.userID }</h4>
                                </Col>
                                <Col>
                                    <h4 style={h4inlinestyle}>{ review.reviewerLName }</h4>
                                </Col>
                                <Col>
                                	<h4 style={h4inlinestyle}>{ review.reviewerFName }</h4>
                                </Col>
                                <Col>
                                    <h4 style={h4inlinestyle}>{ review.dateReviewed }</h4>
                                </Col>
                            </Row>
                        </Container>
                    </p>
                    <Collapse isOpen={this.state.reviews[index].collapsed}>
                        <p style={textareastyle}>{ review.content }</p>
                    </Collapse>
                </p>
            </Container>
        ));
    }
}

const reviewstyle = {
	margin: '15px',
	padding: '15px',
		'background-color': '#FFF',
		'border-radius': '8px',
		'box-shadow': '0px 0px 10px rgba(0, 0, 0, 0.2)'
}

const h3inlinestyle = {
	'text-align': 'left',
}

const h4inlinestyle = {
	'text-align': 'center',
}
	
const textareastyle = {
	'text-align': 'left',
	'overflow-wrap': 'break-word',
	'overflow-y': 'hidden',
	width: '80%' 
}

export default Reviews;
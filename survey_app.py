import streamlit as st
import pandas as pd

class SurveySimilarityApp:
    def __init__(self):
        # Initialize session state if not already done
        if 'selected_question' not in st.session_state:
            st.session_state.selected_question = None

        self.survey_data = {
            "generic_survey": {
                "customer_satisfaction": [
                    "How satisfied are you with our product quality?",
                    "Would you recommend our product to others?",
                    "How likely are you to purchase from us again?"
                ],
                "usability": [
                    "How easy was it to use our product?",
                    "Did you encounter any difficulties?",
                    "Rate the user interface of our product"
                ]
            },
            "similar_questions": {
                "How satisfied are you with our product quality?": [
                    {"survey": "Product Survey 2024", "question": "Rate your satisfaction with product quality", "similarity": 0.85},
                    {"survey": "Customer Feedback", "question": "Are you satisfied with the product?", "similarity": 0.82},
                    {"survey": "Annual Survey", "question": "Product satisfaction rating", "similarity": 0.79}
                ],
                "Would you recommend our product to others?": [
                    {"survey": "Product Survey 2024", "question": "Would you suggest this to others?", "similarity": 0.88},
                    {"survey": "Customer Feedback", "question": "How likely are you to recommend us?", "similarity": 0.84},
                    {"survey": "Annual Survey", "question": "Recommendation likelihood score", "similarity": 0.81}
                ],
                "How likely are you to purchase from us again?": [
                    {"survey": "Product Survey 2024", "question": "Future purchase intention rating", "similarity": 0.87},
                    {"survey": "Customer Feedback", "question": "Will you buy from us again?", "similarity": 0.83},
                    {"survey": "Annual Survey", "question": "Repeat purchase likelihood", "similarity": 0.78}
                ],
                "How easy was it to use our product?": [
                    {"survey": "Product Survey 2024", "question": "How would you rate ease of use?", "similarity": 0.85},
                    {"survey": "User Experience", "question": "Rate the product's usability", "similarity": 0.82},
                    {"survey": "Customer Feedback", "question": "How intuitive was the interface?", "similarity": 0.78}
                ],
                "Did you encounter any difficulties?": [
                    {"survey": "Product Survey 2024", "question": "Were there any problems during usage?", "similarity": 0.86},
                    {"survey": "User Experience", "question": "List any difficulties experienced", "similarity": 0.81},
                    {"survey": "Customer Feedback", "question": "What challenges did you face?", "similarity": 0.77}
                ],
                "Rate the user interface of our product": [
                    {"survey": "User Experience", "question": "Evaluate the UI design", "similarity": 0.87},
                    {"survey": "Product Survey 2024", "question": "Rate the interface design", "similarity": 0.83},
                    {"survey": "Customer Feedback", "question": "UI/UX satisfaction score", "similarity": 0.76}
                ]
            }
        }

    def update_selected_question(self, question):
        st.session_state.selected_question = question

    def run(self):
        st.title("Survey Question Similarity Analysis")

        # Category selection
        categories = list(self.survey_data["generic_survey"].keys())
        categories.insert(0, "all")
        
        selected_category = st.selectbox(
            "Select Question Category",
            categories,
            format_func=lambda x: x.replace("_", " ").title()
        )

        # Similarity threshold
        similarity_threshold = st.slider(
            "Similarity Threshold",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.05
        )

        # Create two columns
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Generic Survey Questions")
            
            # Filter questions by category
            questions_to_show = {}
            if selected_category == "all":
                questions_to_show = self.survey_data["generic_survey"]
            else:
                questions_to_show = {
                    selected_category: self.survey_data["generic_survey"][selected_category]
                }

            # Display generic questions as clickable elements
            for category, questions in questions_to_show.items():
                st.markdown(f"**{category.replace('_', ' ').title()}**")
                for q in questions:
                    # Use a unique key for each button
                    if st.button(
                        q, 
                        key=f"btn_{category}_{q}",
                        on_click=self.update_selected_question,
                        args=(q,)
                    ):
                        pass  # The on_click handler will update the state
                st.markdown("---")

        with col2:
            st.subheader("Similar Questions")
            
            if st.session_state.selected_question:
                selected_q = st.session_state.selected_question
                
                # Show selected question
                st.markdown("**Selected Question:**")
                st.markdown(f"*{selected_q}*")
                st.markdown("---")

                # Get and display similar questions
                if selected_q in self.survey_data["similar_questions"]:
                    similar_questions = self.survey_data["similar_questions"][selected_q]
                    found_matches = False
                    
                    for q in similar_questions:
                        if q["similarity"] >= similarity_threshold:
                            found_matches = True
                            score = q["similarity"]
                            color = (
                                "#d1fae5" if score >= 0.85
                                else "#fef3c7" if score >= 0.75
                                else "#f3f4f6"
                            )
                            
                            st.markdown(f"""
                            <div style='padding: 1rem; 
                                border-radius: 0.5rem; 
                                margin-bottom: 1rem;
                                background-color: {color}'>
                                <p style='color: #666; font-size: 0.875rem; margin-bottom: 0.5rem;'>{q["survey"]}</p>
                                <p style='margin: 0.5rem 0;'>{q["question"]}</p>
                                <p style='font-size: 0.875rem; margin-top: 0.5rem;'>
                                    Similarity: {score*100:.1f}%
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    if not found_matches:
                        st.warning(f"No questions found with similarity ≥ {similarity_threshold*100:.0f}%")
                else:
                    st.info("No similar questions found for this question")
            else:
                st.info("Select a generic question to see similar questions")

        # Color legend
        st.markdown("---")
        st.markdown("**Color Legend:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div style='background-color: #d1fae5; padding: 0.5rem; border-radius: 0.25rem;'>
                High Similarity (≥85%)
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style='background-color: #fef3c7; padding: 0.5rem; border-radius: 0.25rem;'>
                Medium Similarity (75-84%)
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div style='background-color: #f3f4f6; padding: 0.5rem; border-radius: 0.25rem;'>
                Lower Similarity (<75%)
            </div>
            """, unsafe_allow_html=True)

def main():
    app = SurveySimilarityApp()
    app.run()

if __name__ == "__main__":
    main()
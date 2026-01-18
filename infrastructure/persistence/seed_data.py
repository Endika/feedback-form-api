import logging
from datetime import UTC, datetime

from domain.entities.answer import Answer
from domain.entities.form import Form
from domain.entities.question import Question
from domain.entities.response import Response
from domain.repositories.form_repository import FormRepository
from domain.repositories.response_repository import ResponseRepository
from domain.value_objects.form_id import FormId
from domain.value_objects.form_type import FormType
from domain.value_objects.multilingual_text import MultilingualText
from domain.value_objects.question_id import QuestionId
from domain.value_objects.question_type import QuestionType
from domain.value_objects.response_id import ResponseId

logger = logging.getLogger(__name__)


def create_sample_forms() -> list[Form]:
    forms = []

    product_feedback_form = Form(
        id=FormId("sample-product-feedback-001"),
        type=FormType.PRODUCT_FEEDBACK,
        name=MultilingualText(
            {
                "en": "Product Feedback Form",
                "es": "Formulario de Feedback del Producto",
                "fr": "Formulaire de Commentaires sur le Produit",
            }
        ),
        description=MultilingualText(
            {
                "en": "Help us improve our product by sharing your feedback",
                "es": "Ayúdanos a mejorar nuestro producto compartiendo tu feedback",
                "fr": "Aidez-nous à améliorer notre produit en partageant vos commentaires",
            }
        ),
        questions=[
            Question(
                id=QuestionId("q-rating-satisfaction"),
                type=QuestionType.RATING,
                text=MultilingualText(
                    {
                        "en": "How satisfied are you with our product?",
                        "es": "¿Qué tan satisfecho estás con nuestro producto?",
                        "fr": "Dans quelle mesure êtes-vous satisfait de notre produit?",
                    }
                ),
                required=True,
                min_rating=1,
                max_rating=5,
            ),
            Question(
                id=QuestionId("q-text-comments"),
                type=QuestionType.TEXT,
                text=MultilingualText(
                    {
                        "en": "Additional comments",
                        "es": "Comentarios adicionales",
                        "fr": "Commentaires supplémentaires",
                    }
                ),
                required=False,
            ),
        ],
        created_at=datetime.now(tz=UTC),
        updated_at=datetime.now(tz=UTC),
    )
    forms.append(product_feedback_form)

    support_ticket_form = Form(
        id=FormId("sample-support-ticket-001"),
        type=FormType.SUPPORT_TICKET,
        name=MultilingualText(
            {
                "en": "Support Ticket",
                "es": "Ticket de Soporte",
                "fr": "Ticket de Support",
            }
        ),
        description=MultilingualText(
            {
                "en": "Submit a support ticket for assistance",
                "es": "Envía un ticket de soporte para recibir ayuda",
                "fr": "Soumettez un ticket de support pour obtenir de l'aide",
            }
        ),
        questions=[
            Question(
                id=QuestionId("q-text-issue"),
                type=QuestionType.TEXT,
                text=MultilingualText(
                    {
                        "en": "Describe your issue",
                        "es": "Describe tu problema",
                        "fr": "Décrivez votre problème",
                    }
                ),
                required=True,
            ),
            Question(
                id=QuestionId("q-choice-priority"),
                type=QuestionType.MULTIPLE_CHOICE,
                text=MultilingualText(
                    {
                        "en": "Priority",
                        "es": "Prioridad",
                        "fr": "Priorité",
                    }
                ),
                required=True,
                options=[
                    MultilingualText({"en": "Low", "es": "Baja", "fr": "Faible"}),
                    MultilingualText({"en": "Medium", "es": "Media", "fr": "Moyenne"}),
                    MultilingualText({"en": "High", "es": "Alta", "fr": "Élevée"}),
                    MultilingualText({"en": "Urgent", "es": "Urgente", "fr": "Urgente"}),
                ],
            ),
        ],
        created_at=datetime.now(tz=UTC),
        updated_at=datetime.now(tz=UTC),
    )
    forms.append(support_ticket_form)

    survey_form = Form(
        id=FormId("sample-survey-001"),
        type=FormType.SURVEY,
        name=MultilingualText(
            {
                "en": "Customer Satisfaction Survey",
                "es": "Encuesta de Satisfacción del Cliente",
                "fr": "Enquête de Satisfaction Client",
            }
        ),
        description=MultilingualText(
            {
                "en": "Share your thoughts about our service",
                "es": "Comparte tus pensamientos sobre nuestro servicio",
                "fr": "Partagez vos réflexions sur notre service",
            }
        ),
        questions=[
            Question(
                id=QuestionId("q-rating-overall"),
                type=QuestionType.RATING,
                text=MultilingualText(
                    {
                        "en": "Overall satisfaction",
                        "es": "Satisfacción general",
                        "fr": "Satisfaction globale",
                    }
                ),
                required=True,
                min_rating=1,
                max_rating=10,
            ),
            Question(
                id=QuestionId("q-choice-recommend"),
                type=QuestionType.MULTIPLE_CHOICE,
                text=MultilingualText(
                    {
                        "en": "Would you recommend us?",
                        "es": "¿Nos recomendarías?",
                        "fr": "Nous recommanderiez-vous?",
                    }
                ),
                required=True,
                options=[
                    MultilingualText({"en": "Yes", "es": "Sí", "fr": "Oui"}),
                    MultilingualText({"en": "No", "es": "No", "fr": "Non"}),
                    MultilingualText({"en": "Maybe", "es": "Tal vez", "fr": "Peut-être"}),
                ],
            ),
            Question(
                id=QuestionId("q-text-suggestions"),
                type=QuestionType.TEXT,
                text=MultilingualText(
                    {
                        "en": "Suggestions for improvement",
                        "es": "Sugerencias de mejora",
                        "fr": "Suggestions d'amélioration",
                    }
                ),
                required=False,
            ),
        ],
        created_at=datetime.now(tz=UTC),
        updated_at=datetime.now(tz=UTC),
    )
    forms.append(survey_form)

    return forms


def create_sample_responses(form: Form) -> list[Response]:
    responses = []

    if str(form.id) == "sample-product-feedback-001":
        response1 = Response(
            id=ResponseId("response-sample-001"),
            form_id=form.id,
            answers=[
                Answer(question_id=QuestionId("q-rating-satisfaction"), value=5),
                Answer(
                    question_id=QuestionId("q-text-comments"),
                    value="Great product! Very satisfied with the quality.",
                ),
            ],
            tags={"campaign": "summer2024", "source": "email", "group": "premium_users"},
            user_id="user-sample-001",
            submitted_at=datetime.now(tz=UTC),
        )
        responses.append(response1)

        response2 = Response(
            id=ResponseId("response-sample-002"),
            form_id=form.id,
            answers=[
                Answer(question_id=QuestionId("q-rating-satisfaction"), value=4),
                Answer(question_id=QuestionId("q-text-comments"), value="Good overall experience."),
            ],
            tags={"campaign": "summer2024", "source": "web", "group": "regular_users"},
            user_id="user-sample-002",
            submitted_at=datetime.now(tz=UTC),
        )
        responses.append(response2)

    elif str(form.id) == "sample-support-ticket-001":
        response = Response(
            id=ResponseId("response-sample-003"),
            form_id=form.id,
            answers=[
                Answer(
                    question_id=QuestionId("q-text-issue"),
                    value="Having trouble logging in to my account.",
                ),
                Answer(question_id=QuestionId("q-choice-priority"), value="Medium"),
            ],
            tags={"source": "web"},
            user_id="user-sample-003",
            submitted_at=datetime.now(tz=UTC),
        )
        responses.append(response)

    return responses


async def seed_database(
    form_repository: FormRepository,
    response_repository: ResponseRepository,
) -> None:
    existing_forms = await form_repository.get_all()
    if existing_forms:
        logger.info(
            "Database already contains data, skipping seed",
            extra={"existing_forms_count": len(existing_forms)},
        )
        return

    logger.info("Seeding database with sample data")
    forms = create_sample_forms()

    for form in forms:
        await form_repository.create(form)
        responses = create_sample_responses(form)
        for response in responses:
            await response_repository.create(response)

    logger.info(
        "Database seeded successfully",
        extra={
            "forms_created": len(forms),
            "responses_created": sum(len(create_sample_responses(f)) for f in forms),
        },
    )

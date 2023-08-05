"""Annotation."""
import logging
import re
import urllib
from typing import Dict, Optional, Tuple, Union

import requests

from pymetadata.core.xref import CrossReference, is_url
from pymetadata.identifiers.miriam import BQB, BQM
from pymetadata.identifiers.registry import Registry
from pymetadata.ontologies.ols import ONTOLOGIES, OLSQuery


REGISTRY = Registry()
OLS_QUERY = OLSQuery(ontologies=ONTOLOGIES)


IDENTIFIERS_ORG_PREFIX = "https://identifiers.org"
IDENTIFIERS_ORG_PATTERN1 = re.compile(r"^https?://identifiers.org/(.+?)/(.+)")
IDENTIFIERS_ORG_PATTERN2 = re.compile(r"^https?://identifiers.org/(.+)")
MIRIAM_URN_PATTERN = re.compile(r"^urn:miriam:(.+):(.+)")

logger = logging.getLogger(__name__)


class RDFAnnotation:
    """RDFAnnotation class.

    Basic storage of annotation information. This consists of the relation
    and the the resource.
    The annotations can be attached to other objects thereby forming
    triples which can be converted to RDF.

    Resource can be either:
        - `http(s)://identifiers.org/collection/term`, i.e., a identifiers.org URI
        - `collection/term`, i.e., the combination of collection and term
        - `http(s)://arbitrary.url`, an arbitrary URL
        - urn:miriam:uniprot:P03023
    """

    def __init__(self, qualifier: Union[BQB, BQM], resource: str):

        self.qualifier: Union[BQB, BQM] = qualifier
        self.collection: Optional[str] = None
        self.term: Optional[str] = None

        if not qualifier:
            raise ValueError(
                f"MIRIAM qualifiers are required for rdf annotation, but no "
                f"qualifier for resource '{resource}' was provided."
            )
        if not resource:
            raise ValueError(
                f"resource is required for annotation, but resource is emtpy "
                f"'{qualifier} {resource}'."
            )
        if not isinstance(resource, str):
            raise ValueError(
                f"resource must be string, but found '{resource} {type(resource)}'."
            )

        # handle urls
        if resource.startswith("http"):
            match1 = IDENTIFIERS_ORG_PATTERN1.match(resource)
            if match1:
                # handle identifiers.org pattern
                self.collection, self.term = match1.group(1), match1.group(2)

            if not self.collection:
                # test new short pattern
                match2 = IDENTIFIERS_ORG_PATTERN2.match(resource)
                if match2:
                    tokens = match2.group(1).split(":")
                    if len(tokens) == 2:
                        self.collection = tokens[0].lower()
                        self.term = match2.group(1)
                    else:
                        logger.warning(
                            f"Identifiers.org URL does not conform to new"
                            f"short pattern: {resource}"
                        )

            if not self.collection:
                # other urls are directly stored as resources without collection
                self.collection = None
                self.term = resource
                logger.warning(
                    f"{resource} does not conform to "
                    f"http(s)://identifiers.org/collection/id or http(s)://identifiers.org/id",
                )
        elif resource.startswith("urn:miriam:"):
            match3 = MIRIAM_URN_PATTERN.match(resource)
            if match3:
                self.collection, self.term = match3.group(1), match3.group(2)
                logger.warning(
                    f"Deprecated urn pattern `{resource}`, use " f"{self.resource}"
                )

        else:
            # handle short notation
            tokens = resource.split("/")
            if len(tokens) == 2:
                self.collection = tokens[0]
                self.term = "/".join(tokens[1:])
            elif len(tokens) == 1 and ":" in tokens[0]:
                self.collection = tokens[0].split(":")[0].lower()
                self.term = tokens[0]

            if len(tokens) < 2 and not self.collection:
                logger.error(
                    f"Resource `{resource}` could not be split in collection and term. "
                    f"A given resource must be of the form "
                    f"`collection/term` or an url starting with "
                    f"`http(s)://`)"
                )
                self.collection = None
                self.term = resource

        self.validate()

    @staticmethod
    def from_tuple(t: Tuple[Union[BQB, BQM], str]) -> "RDFAnnotation":
        """Construct from tuple."""
        qualifier, resource = t[0], t[1]
        return RDFAnnotation(qualifier=qualifier, resource=resource)

    def from_collection_term(
        qualifier: Union[BQB, BQM], collection: str, term: str
    ) -> "RDFAnnotation":
        """Construct from tuple."""

        return RDFAnnotation(qualifier=qualifier, resource=f"{collection}/{term}")

    @property
    def resource(self) -> Optional[str]:
        """Resource for annotation."""
        if self.collection:
            if self.term.startswith(f"{self.collection.upper()}:"):
                return f"{IDENTIFIERS_ORG_PREFIX}/{self.term}"
            else:
                return f"{IDENTIFIERS_ORG_PREFIX}/{self.collection}/{self.term}"
        else:
            return self.term

    def __repr__(self):
        """Get representation string."""
        return f"RDFAnnotation({self.qualifier}|{self.collection}|{self.term})"

    def to_dict(self):
        """Convert to dict."""
        return {
            "qualifier": self.qualifier.value,  # FIXME use enums!
            "collection": self.collection,
            "term": self.term,
        }

    @staticmethod
    def check_term(collection: str, term: str) -> bool:
        """Check that term follows id pattern for collection.

        Uses the Identifiers collection information.
        """
        namespace = REGISTRY.ns_dict.get(collection, None)
        if not namespace:
            raise ValueError(
                f"MIRIAM collection `{collection}` does not exist for term `{term}`"
            )

        p = re.compile(namespace.pattern)
        m = p.match(term)
        if not m:
            raise ValueError(
                f"Term `{term}` did not match pattern "
                f"`{namespace.pattern}` for collection `{collection}`."
            )
            return False

        return True

    @staticmethod
    def check_qualifier(qualifier: Union[BQB, BQM]) -> None:
        """Check that the qualifier is an allowed qualifier.

        :param qualifier:
        :return:
        """
        if not isinstance(qualifier, (BQB, BQM)):
            supported_qualifiers = [e.value for e in BQB] + [e.value for e in BQM]

            raise ValueError(
                f"qualifier `{qualifier}` is not in supported qualifiers: "
                f"`{supported_qualifiers}`"
            )

    def validate(self) -> None:
        """Validate annotation."""
        self.check_qualifier(self.qualifier)
        if self.collection:
            self.check_term(collection=self.collection, term=self.term)


class RDFAnnotationData(RDFAnnotation):
    """Annotation with resolved information.

    queries for the resource should happen here;
    this resolves additional information.
    """

    def __init__(self, annotation: RDFAnnotation):

        self.qualifier = annotation.qualifier
        self.collection = annotation.collection
        self.term = annotation.term
        self.url: str = None
        self.description: str = None
        self.label: str = None
        self.synonyms = []
        self.xrefs = []

        if self.collection:

            # register MIRIAM xrefs
            namespace = REGISTRY.ns_dict.get(self.collection)
            namespace_embedded = namespace.namespaceEmbeddedInLui
            # print("-" * 80)
            # print(namespace.prefix, "embedded=", namespace_embedded)

            for resource in namespace.resources:  # Resource

                # create url
                url = resource.urlPattern
                term = self.term

                # remove prefix
                if namespace_embedded:
                    term = term[len(namespace.prefix) + 1 :]

                # urlencode term
                term = urllib.parse.quote(term)

                # create url
                url = url.replace("{$Id}", term)
                url = url.replace("{$id}", term)
                url = url.replace(
                    f"{namespace.prefix.upper}:",
                    urllib.parse.quote(f"{namespace.prefix.upper}:"),
                )

                if not self.url:
                    # set url to first resource url
                    self.url = url

                # print(url)
                _xref = CrossReference(name=resource.name, accession=self.term, url=url)
                valid = _xref.validate() and is_url(self.url)
                if valid:
                    self.xrefs.append(_xref)

        # query OLS information
        self.query_ols()

    def __repr__(self):
        """Get representation string."""
        return f"RDFAnnotationData({self.collection}|{self.term}|{self.label}|{self.description}|{self.synonyms}|{self.xrefs})"

    def to_dict(self):
        """Convert to dict."""
        return {
            "qualifier": self.qualifier.value,
            "collection": self.collection,
            "term": self.term,
            "description": self.description,
            "label": self.label,
            "url": self.url,
            # synonyms and xrefs are not serialized
        }

    def query_ols(self):
        """Query ontology lookup service."""
        try:
            d = OLS_QUERY.query_ols(ontology=self.collection, term=self.term)
        except requests.HTTPError as err:
            logger.error(err)
            d = {}

        info = OLS_QUERY.process_response(d)
        print(info)
        self.info = info
        if info is not None:
            if self.label is None:
                self.label = info.get("label")

            if self.description is None:
                self.description = info.get("description")

            self.synonyms = info["synonyms"]
            self.xrefs = info["xrefs"]

        return info


# TODO: caching of information; fill local storage nosql
# caching: https://realpython.com/python-memcache-efficient-caching/


if __name__ == "__main__":
    for annotation in [
        RDFAnnotation(
            qualifier=BQB.IS, resource="https://en.wikipedia.org/wiki/Cytosol"
        ),
        RDFAnnotation(
            qualifier=BQB.IS_VERSION_OF, resource="urn:miriam:uniprot:P03023"
        ),
        RDFAnnotation(
            qualifier=BQB.IS_VERSION_OF,
            resource="https://identifiers.org/go/GO:0005829",
        ),
        RDFAnnotation(
            qualifier=BQB.IS_VERSION_OF, resource="http://identifiers.org/go/GO:0005829"
        ),
        RDFAnnotation(
            qualifier=BQB.IS_VERSION_OF, resource="https://identifiers.org/GO:0005829"
        ),
        RDFAnnotation(
            qualifier=BQB.IS_VERSION_OF, resource="http://identifiers.org/GO:0005829"
        ),
        RDFAnnotation(qualifier=BQB.IS_VERSION_OF, resource="bto/BTO:0000089"),
        RDFAnnotation(qualifier=BQB.IS_VERSION_OF, resource="BTO:0000089"),
        RDFAnnotation(qualifier=BQB.IS_VERSION_OF, resource="chebi/CHEBI:000012"),
    ]:
        print(annotation, annotation.resource)

        data = RDFAnnotationData(annotation)
        print(data)

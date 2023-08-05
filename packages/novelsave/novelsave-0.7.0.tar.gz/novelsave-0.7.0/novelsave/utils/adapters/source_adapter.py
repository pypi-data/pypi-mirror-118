from novelsave_sources import models as sm
from novelsave.core import dtos


class SourceAdapter(object):
    """adapter responsible for converting models from view_models to source and vice versa"""

    def novel_to_internal(self, novel: sm.Novel) -> dtos.NovelDTO:
        """convert novel from internal to source"""

        arguments = {
            key: value
            for key, value in vars(novel).items()
            if key in {'title', 'url', 'author', 'synopsis', 'thumbnail_url', 'lang'}
        }

        return dtos.NovelDTO(id=None, **arguments)

    def novel_to_external(self, novel: dtos.NovelDTO) -> sm.Novel:
        """convert novel from source to internal"""

        arguments = {
            key: value
            for key, value in vars(novel).items()
            if key in {'title', 'url', 'author', 'synopsis', 'thumbnail_url', 'lang'}
        }

        return sm.Novel(**arguments)

    def chapter_to_internal(self, chapter: sm.Chapter) -> dtos.ChapterDTO:
        """convert chapter from source to internal"""

        return dtos.ChapterDTO(
            index=chapter.index,
            title=chapter.title,
            url=chapter.url,
            content=chapter.paragraphs,
            volume=chapter.volume,
        )

    def chapter_to_external(self, chapter: dtos.ChapterDTO) -> sm.Chapter:
        """convert chapter from internal to source"""

        return sm.Chapter(
            index=chapter.index,
            title=chapter.title,
            url=chapter.url,
            paragraphs=chapter.content,
            volume=chapter.volume,
        )

    def metadata_to_internal(self, metadata: sm.Metadata) -> dtos.MetaDataDTO:
        """convert metadata from source to internal"""

        return dtos.MetaDataDTO(
            name=metadata.name,
            value=metadata.value,
            namespace=metadata.namespace,
            others=metadata.others,
        )

    def metadata_to_external(self, metadata: dtos.MetaDataDTO) -> sm.Metadata:
        """convert metadata from internal to source"""

        return sm.Metadata(
            name=metadata.name,
            value=metadata.value,
            namespace=metadata.namespace,
            others=metadata.others,
        )

    def chapter_content_to_internal(self, source_chapter: sm.Chapter, internal_chapter: dtos.ChapterDTO):
        """map content from source chapter to internal chapter"""
        internal_chapter.content = source_chapter.paragraphs

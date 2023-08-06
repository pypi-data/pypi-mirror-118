#!/usr/bin/env python3
# Copyright (C) 2019-2021 All rights reserved.
# FILENAME: backends/base.py
# VERSION: 	0.0.1
# CREATED: 	2021-08-31 16:10
# AUTHOR: 	Aekasitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Standard Packages ###
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from uuid import uuid4 as uuid

class BackstageSeshBackend(ABC):
  '''
  Base class for session backends
  '''

  @abstractmethod
  async def read(self, session_id: str) -> Dict[str, Any]:
    '''
    Read session data from the storage.
    '''
    raise NotImplementedError

  @abstractmethod
  async def write(self, data: Dict, session_id: Optional[str] = None) -> str:
    '''
    Write session data to the storage.
    '''
    raise NotImplementedError

  @abstractmethod
  async def remove(self, session_id: str) -> None:
    '''
    Remove session data from the storage.
    '''
    raise NotImplementedError

  @abstractmethod
  async def exists(self, session_id: str) -> bool:
    '''
    Test if storage contains session data for a given session_id.
    '''
    raise NotImplementedError

  async def generate_id(self) -> str:
    '''
    Generate a new session id.
    '''
    return str(uuid())
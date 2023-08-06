from enum import Enum
from typing import Type

import pydantic
from classiq_interface.generator.function_params import FunctionParams
from qiskit import circuit as qiskit_circuit
from qiskit import qasm as qiskit_qasm


class CustomFunctionInputs(Enum):
    CUSTOM_FUNCTION_INPUT = "CUSTOM_FUNCTION_INPUT"


class CustomFunctionOutputs(Enum):
    CUSTOM_FUNCTION_OUTPUT = "CUSTOM_FUNCTION_OUTPUT"


class CustomFunction(FunctionParams):
    """
    Facilitates the creation of a user-defined custom function
    """

    single_implementation_qasm_circuit_string: pydantic.constr(
        min_length=1
    ) = pydantic.Field(description="The QASM code of a custom function")

    @pydantic.validator("single_implementation_qasm_circuit_string")
    def validate_single_implementation_qasm_circuit_string(
        cls, single_implementation_qasm_circuit_string
    ):
        try:
            qiskit_circuit.QuantumCircuit.from_qasm_str(
                single_implementation_qasm_circuit_string
            )
        except qiskit_qasm.exceptions.QasmError:  # The qiskit error is often extremely uninformative
            raise ValueError("The QASM string is not a valid quantum circuit.")
        return single_implementation_qasm_circuit_string

    _input_names: Type[Enum] = pydantic.PrivateAttr(default=CustomFunctionInputs)
    _output_names: Type[Enum] = pydantic.PrivateAttr(default=CustomFunctionOutputs)
